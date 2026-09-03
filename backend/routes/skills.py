from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from extensions import db
from models.skill import Skill
from utils.auth import token_required

skills_bp = Blueprint("skills", __name__)


@skills_bp.route("", methods=["GET"])
@skills_bp.route("/", methods=["GET"])
def get_skills():
    """
    Lists and searches skills with optional filters.
    Query params:
      - q or search: search term matching skill_name or description
      - type: 'teach' or 'learn'
      - user_id: filter by specific user
    """
    query = Skill.query

    # Search keyword filter
    search_term = (request.args.get("q") or request.args.get("search") or "").strip()
    if search_term:
        term_pattern = f"%{search_term}%"
        query = query.filter(
            or_(
                Skill.skill_name.ilike(term_pattern),
                Skill.description.ilike(term_pattern)
            )
        )

    # Skill type filter ('teach' vs 'learn')
    skill_type = (request.args.get("type") or "").strip().lower()
    if skill_type:
        query = query.filter(Skill.skill_type == skill_type)

    # Creator / User ID filter
    user_id = request.args.get("user_id")
    if user_id:
        try:
            query = query.filter(Skill.user_id == int(user_id))
        except ValueError:
            return jsonify({"error": "user_id must be a valid integer."}), 400

    skills = query.order_by(Skill.created_at.desc()).all()

    return jsonify({
        "count": len(skills),
        "skills": [skill.to_dict(include_owner=True) for skill in skills]
    }), 200


@skills_bp.route("/<int:skill_id>", methods=["GET"])
def get_skill_details(skill_id: int):
    """
    Retrieves full details for a single skill by ID.
    """
    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({"error": f"Skill with ID {skill_id} not found."}), 404

    return jsonify({
        "skill": skill.to_dict(include_owner=True)
    }), 200


@skills_bp.route("", methods=["POST"])
@skills_bp.route("/", methods=["POST"])
@token_required
def create_skill(current_user):
    """
    Creates a new skill offering or learning interest for the authenticated user.
    """
    data = request.get_json() or {}
    skill_name = (data.get("skill_name") or "").strip()
    skill_type = (data.get("skill_type") or "").strip().lower()
    description = (data.get("description") or "").strip() or None

    # Validations
    if not skill_name:
        return jsonify({"error": "Skill name is required."}), 400
    if len(skill_name) < 2 or len(skill_name) > 100:
        return jsonify({"error": "Skill name must be between 2 and 100 characters."}), 400

    if not skill_type or skill_type not in ["teach", "learn"]:
        return jsonify({
            "error": "Skill type is required and must be either 'teach' or 'learn'."
        }), 400

    try:
        skill = Skill(
            user_id=current_user.id,
            skill_name=skill_name,
            skill_type=skill_type,
            description=description
        )
        db.session.add(skill)
        db.session.commit()

        return jsonify({
            "message": "Skill created successfully!",
            "skill": skill.to_dict(include_owner=True)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create skill. Please try again."}), 500


@skills_bp.route("/<int:skill_id>", methods=["PUT"])
@token_required
def update_skill(current_user, skill_id: int):
    """
    Updates an existing skill. Only the creator can modify their skill.
    """
    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({"error": f"Skill with ID {skill_id} not found."}), 404

    if skill.user_id != current_user.id:
        return jsonify({
            "error": "Forbidden. You can only modify your own skills."
        }), 403

    data = request.get_json() or {}

    if "skill_name" in data:
        name = (data.get("skill_name") or "").strip()
        if not name or len(name) < 2 or len(name) > 100:
            return jsonify({"error": "Skill name must be between 2 and 100 characters."}), 400
        skill.skill_name = name

    if "skill_type" in data:
        stype = (data.get("skill_type") or "").strip().lower()
        if stype not in ["teach", "learn"]:
            return jsonify({"error": "Skill type must be either 'teach' or 'learn'."}), 400
        skill.skill_type = stype

    if "description" in data:
        desc = (data.get("description") or "").strip()
        skill.description = desc if desc else None

    try:
        db.session.commit()
        return jsonify({
            "message": "Skill updated successfully!",
            "skill": skill.to_dict(include_owner=True)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update skill."}), 500


@skills_bp.route("/<int:skill_id>", methods=["DELETE"])
@token_required
def delete_skill(current_user, skill_id: int):
    """
    Deletes a skill. Only the creator can delete their skill.
    """
    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({"error": f"Skill with ID {skill_id} not found."}), 404

    if skill.user_id != current_user.id:
        return jsonify({
            "error": "Forbidden. You can only delete your own skills."
        }), 403

    try:
        db.session.delete(skill)
        db.session.commit()
        return jsonify({
            "message": "Skill deleted successfully!",
            "deleted_id": skill_id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete skill."}), 500
