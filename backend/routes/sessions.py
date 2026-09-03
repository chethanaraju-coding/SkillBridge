import uuid
from datetime import datetime, date, time
from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from extensions import db
from models.user import User
from models.skill import Skill
from models.session import LearningSession
from utils.auth import token_required

sessions_bp = Blueprint("sessions", __name__)


def _parse_time(time_str: str) -> time:
    """Parses time string in HH:MM or HH:MM:SS format."""
    time_str = time_str.strip()
    for fmt in ("%H:%M", "%H:%M:%S"):
        try:
            return datetime.strptime(time_str, fmt).time()
        except ValueError:
            pass
    raise ValueError(f"Invalid time format '{time_str}'. Expected 'HH:MM'.")


@sessions_bp.route("", methods=["POST"])
@sessions_bp.route("/", methods=["POST"])
@token_required
def create_session(current_user):
    """
    Schedules a new learning/mentoring session.
    Validations:
      - Current user must be either the teacher or learner
      - Teacher and learner cannot be the same user
      - Teacher, learner, and skill must exist in the database
      - Date cannot be in the past
      - End time must be after start time (if provided)
    """
    data = request.get_json() or {}
    teacher_id = data.get("teacher_id")
    learner_id = data.get("learner_id")
    skill_id = data.get("skill_id")
    session_date_str = (data.get("session_date") or "").strip()
    start_time_str = (data.get("start_time") or "").strip()
    end_time_str = (data.get("end_time") or "").strip()
    meeting_link = (data.get("meeting_link") or "").strip()

    # Field presence checks
    if not teacher_id or not learner_id or not skill_id or not session_date_str or not start_time_str:
        return jsonify({
            "error": "Missing required fields: teacher_id, learner_id, skill_id, session_date, start_time."
        }), 400

    try:
        teacher_id = int(teacher_id)
        learner_id = int(learner_id)
        skill_id = int(skill_id)
    except ValueError:
        return jsonify({"error": "teacher_id, learner_id, and skill_id must be valid integers."}), 400

    # User authorization: current user must be participant
    if current_user.id not in [teacher_id, learner_id]:
        return jsonify({
            "error": "Forbidden. You can only schedule sessions where you are the teacher or learner."
        }), 403

    if teacher_id == learner_id:
        return jsonify({"error": "Teacher and learner cannot be the same user."}), 400

    # Existence checks
    teacher = User.query.get(teacher_id)
    if not teacher:
        return jsonify({"error": f"Teacher with ID {teacher_id} not found."}), 404

    learner = User.query.get(learner_id)
    if not learner:
        return jsonify({"error": f"Learner with ID {learner_id} not found."}), 404

    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({"error": f"Skill with ID {skill_id} not found."}), 404

    # Date parsing & validation
    try:
        parsed_date = datetime.strptime(session_date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid session_date format. Expected 'YYYY-MM-DD'."}), 400

    if parsed_date < date.today():
        return jsonify({"error": "Session date cannot be in the past."}), 400

    # Time parsing & validation
    try:
        parsed_start = _parse_time(start_time_str)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    parsed_end = None
    if end_time_str:
        try:
            parsed_end = _parse_time(end_time_str)
            if parsed_end <= parsed_start:
                return jsonify({"error": "end_time must be after start_time."}), 400
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    # Meeting link generation if not provided
    if not meeting_link:
        meeting_link = f"https://meet.jit.si/skillbridge-{uuid.uuid4().hex[:12]}"
    elif len(meeting_link) > 255:
        return jsonify({"error": "meeting_link must not exceed 255 characters."}), 400

    try:
        session = LearningSession(
            teacher_id=teacher_id,
            learner_id=learner_id,
            skill_id=skill_id,
            session_date=parsed_date,
            start_time=parsed_start,
            end_time=parsed_end,
            status="scheduled",
            meeting_link=meeting_link
        )
        db.session.add(session)
        db.session.commit()

        return jsonify({
            "message": "Learning session scheduled successfully!",
            "session": session.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to schedule session."}), 500


@sessions_bp.route("", methods=["GET"])
@sessions_bp.route("/", methods=["GET"])
@token_required
def get_sessions(current_user):
    """
    Lists sessions for the authenticated user (as teacher or learner).
    Query params:
      - status: 'scheduled', 'completed', 'cancelled'
      - role: 'teacher' or 'learner'
    """
    status_filter = (request.args.get("status") or "").strip().lower()
    role_filter = (request.args.get("role") or "").strip().lower()

    query = LearningSession.query

    if role_filter == "teacher":
        query = query.filter(LearningSession.teacher_id == current_user.id)
    elif role_filter == "learner":
        query = query.filter(LearningSession.learner_id == current_user.id)
    else:
        query = query.filter(
            or_(
                LearningSession.teacher_id == current_user.id,
                LearningSession.learner_id == current_user.id
            )
        )

    if status_filter:
        query = query.filter(LearningSession.status == status_filter)

    sessions = query.order_by(
        LearningSession.session_date.asc(),
        LearningSession.start_time.asc()
    ).all()

    return jsonify({
        "count": len(sessions),
        "sessions": [s.to_dict() for s in sessions]
    }), 200


@sessions_bp.route("/<int:session_id>", methods=["GET"])
@token_required
def get_session_details(current_user, session_id: int):
    """
    Retrieves full details for a single session.
    User must be a participant (teacher or learner).
    """
    session = LearningSession.query.get(session_id)
    if not session:
        return jsonify({"error": f"Session with ID {session_id} not found."}), 404

    if current_user.id not in [session.teacher_id, session.learner_id]:
        return jsonify({"error": "Forbidden. You are not a participant in this session."}), 403

    return jsonify({"session": session.to_dict()}), 200


@sessions_bp.route("/<int:session_id>", methods=["PUT"])
@token_required
def update_session(current_user, session_id: int):
    """
    Updates session status (completed/cancelled), meeting link, or schedule.
    Only participants may update the session.
    """
    session = LearningSession.query.get(session_id)
    if not session:
        return jsonify({"error": f"Session with ID {session_id} not found."}), 404

    if current_user.id not in [session.teacher_id, session.learner_id]:
        return jsonify({"error": "Forbidden. You are not a participant in this session."}), 403

    data = request.get_json() or {}

    # Status update
    if "status" in data:
        new_status = (data.get("status") or "").strip().lower()
        if new_status not in ["scheduled", "completed", "cancelled"]:
            return jsonify({
                "error": "status must be one of: 'scheduled', 'completed', 'cancelled'."
            }), 400
        session.status = new_status

    # Meeting link update
    if "meeting_link" in data:
        link = (data.get("meeting_link") or "").strip()
        if len(link) > 255:
            return jsonify({"error": "meeting_link must not exceed 255 characters."}), 400
        session.meeting_link = link if link else None

    # Rescheduling date
    if "session_date" in data:
        try:
            parsed_date = datetime.strptime(data["session_date"].strip(), "%Y-%m-%d").date()
            session.session_date = parsed_date
        except ValueError:
            return jsonify({"error": "Invalid session_date. Expected 'YYYY-MM-DD'."}), 400

    # Rescheduling start/end time
    if "start_time" in data:
        try:
            session.start_time = _parse_time(data["start_time"])
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    if "end_time" in data:
        try:
            parsed_end = _parse_time(data["end_time"]) if data["end_time"] else None
            session.end_time = parsed_end
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    try:
        db.session.commit()
        return jsonify({
            "message": "Session updated successfully!",
            "session": session.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update session."}), 500
