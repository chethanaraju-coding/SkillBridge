from flask import Blueprint, request, jsonify
from extensions import db
from models.skill import Skill
from models.skill_request import SkillRequest
from utils.auth import token_required

requests_bp = Blueprint("requests", __name__)


@requests_bp.route("", methods=["POST"])
@requests_bp.route("/", methods=["POST"])
@token_required
def create_request(current_user):
    """
    Creates a new skill learning/exchange request.
    Validations:
      - skill_id must exist
      - cannot request one's own skill
      - cannot have duplicate active (pending) request for the same skill
    """
    data = request.get_json() or {}
    skill_id = data.get("skill_id")
    message = (data.get("message") or "").strip() or None

    if not skill_id:
        return jsonify({"error": "skill_id is required."}), 400

    try:
        skill_id = int(skill_id)
    except ValueError:
        return jsonify({"error": "skill_id must be a valid integer."}), 400

    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({"error": f"Skill with ID {skill_id} not found."}), 404

    # Prevent requesting one's own skill
    if skill.user_id == current_user.id:
        return jsonify({"error": "You cannot request your own skill."}), 400

    # Prevent duplicate pending requests
    existing_pending = SkillRequest.query.filter_by(
        requester_id=current_user.id,
        skill_id=skill.id,
        status="pending"
    ).first()

    if existing_pending:
        return jsonify({
            "error": "You already have a pending request for this skill."
        }), 409

    try:
        skill_req = SkillRequest(
            requester_id=current_user.id,
            skill_id=skill.id,
            message=message,
            status="pending"
        )
        db.session.add(skill_req)
        db.session.commit()

        return jsonify({
            "message": "Skill request submitted successfully!",
            "request": skill_req.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to submit skill request."}), 500


@requests_bp.route("", methods=["GET"])
@requests_bp.route("/", methods=["GET"])
@token_required
def get_requests(current_user):
    """
    Retrieves skill requests for the authenticated user.
    Query parameters:
      - type: 'incoming', 'outgoing', or omit for both
      - status: 'pending', 'accepted', 'rejected', 'cancelled'
    """
    req_type = (request.args.get("type") or "").strip().lower()
    status_filter = (request.args.get("status") or "").strip().lower()

    # Outgoing: Requests created by current_user
    outgoing_query = SkillRequest.query.filter_by(requester_id=current_user.id)
    if status_filter:
        outgoing_query = outgoing_query.filter_by(status=status_filter)

    # Incoming: Requests sent to skills owned by current_user
    incoming_query = SkillRequest.query.join(Skill).filter(Skill.user_id == current_user.id)
    if status_filter:
        incoming_query = incoming_query.filter(SkillRequest.status == status_filter)

    if req_type == "incoming":
        incoming = incoming_query.order_by(SkillRequest.created_at.desc()).all()
        return jsonify({
            "requests": [r.to_dict() for r in incoming],
            "count": len(incoming)
        }), 200

    if req_type == "outgoing":
        outgoing = outgoing_query.order_by(SkillRequest.created_at.desc()).all()
        return jsonify({
            "requests": [r.to_dict() for r in outgoing],
            "count": len(outgoing)
        }), 200

    # Default: Return categorized incoming and outgoing
    incoming = incoming_query.order_by(SkillRequest.created_at.desc()).all()
    outgoing = outgoing_query.order_by(SkillRequest.created_at.desc()).all()

    return jsonify({
        "incoming": [r.to_dict() for r in incoming],
        "outgoing": [r.to_dict() for r in outgoing],
        "total_incoming": len(incoming),
        "total_outgoing": len(outgoing)
    }), 200


@requests_bp.route("/<int:request_id>", methods=["PUT"])
@token_required
def update_request_status(current_user, request_id: int):
    """
    Updates the status of a skill request.
    Allowed transitions:
      - Receiver (skill owner): 'accepted', 'rejected'
      - Sender (requester): 'cancelled'
    """
    skill_req = SkillRequest.query.get(request_id)
    if not skill_req:
        return jsonify({"error": f"Skill request with ID {request_id} not found."}), 404

    data = request.get_json() or {}
    new_status = (data.get("status") or "").strip().lower()
    valid_statuses = ["accepted", "rejected", "cancelled"]

    if not new_status or new_status not in valid_statuses:
        return jsonify({
            "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}."
        }), 400

    # Cannot modify already finalized request
    if skill_req.status in ["accepted", "rejected", "cancelled"]:
        return jsonify({
            "error": f"Cannot modify request because it is already '{skill_req.status}'."
        }), 400

    skill_owner_id = skill_req.skill.user_id if skill_req.skill else None

    # Receiver logic (Skill Owner)
    if current_user.id == skill_owner_id:
        if new_status not in ["accepted", "rejected"]:
            return jsonify({
                "error": "As the skill owner, you can only set status to 'accepted' or 'rejected'."
            }), 400

    # Sender logic (Requester)
    elif current_user.id == skill_req.requester_id:
        if new_status != "cancelled":
            return jsonify({
                "error": "As the requester, you can only cancel your pending request."
            }), 400

    else:
        return jsonify({
            "error": "Forbidden. You are not authorized to modify this request."
        }), 403

    try:
        skill_req.status = new_status
        db.session.commit()

        return jsonify({
            "message": f"Skill request status updated to '{new_status}'.",
            "request": skill_req.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update request status."}), 500
