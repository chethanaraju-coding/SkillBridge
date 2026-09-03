from flask import Blueprint, request, jsonify
from collections import defaultdict
from models.user import User
from models.skill import Skill
from utils.auth import token_required

matches_bp = Blueprint("matches", __name__)


def _normalize_name(name: str) -> str:
    """Normalizes skill name for fuzzy matching."""
    return "".join(c.lower() for c in name if c.isalnum())


def _is_match(skill_a: str, skill_b: str) -> bool:
    """
    Determines if two skill titles represent a match.
    Supports exact, sub-string, or normalized equivalence.
    """
    if not skill_a or not skill_b:
        return False

    norm_a = _normalize_name(skill_a)
    norm_b = _normalize_name(skill_b)

    if norm_a == norm_b:
        return True

    # Substring matching with minimum meaningful length
    if len(norm_a) >= 3 and len(norm_b) >= 3:
        if norm_a in norm_b or norm_b in norm_a:
            return True

    return False


@matches_bp.route("", methods=["GET"])
@matches_bp.route("/", methods=["GET"])
@token_required
def get_matches(current_user):
    """
    Finds skill exchange matches and mentor/learner pairings for the current user.
    Mutual Exchange Match:
      - Current user can teach X and wants to learn Y
      - Matched user can teach Y and wants to learn X
    """
    # 1. Fetch current user's skills
    my_teaches = Skill.query.filter_by(user_id=current_user.id, skill_type="teach").all()
    my_learns = Skill.query.filter_by(user_id=current_user.id, skill_type="learn").all()

    # 2. Fetch all other users' skills
    other_skills = Skill.query.filter(Skill.user_id != current_user.id).all()

    user_skills_map = defaultdict(lambda: {"user": None, "teach": [], "learn": []})
    for s in other_skills:
        user_skills_map[s.user_id]["user"] = s.owner
        if s.skill_type == "teach":
            user_skills_map[s.user_id]["teach"].append(s)
        elif s.skill_type == "learn":
            user_skills_map[s.user_id]["learn"].append(s)

    exchange_matches = []
    mentor_matches = []
    learner_matches = []

    for other_id, data in user_skills_map.items():
        other_user = data["user"]
        other_teaches = data["teach"]
        other_learns = data["learn"]

        if not other_user:
            continue

        # Check for mutual exchange match
        found_exchange = False
        for my_t in my_teaches:
            for their_l in other_learns:
                if _is_match(my_t.skill_name, their_l.skill_name):
                    # Current user can teach what other wants
                    # Now check if other can teach what current user wants
                    for their_t in other_teaches:
                        for my_l in my_learns:
                            if _is_match(their_t.skill_name, my_l.skill_name):
                                exchange_matches.append({
                                    "matched_user": other_user.to_dict(),
                                    "you_teach": my_t.to_dict(include_owner=False),
                                    "they_learn": their_l.to_dict(include_owner=False),
                                    "they_teach": their_t.to_dict(include_owner=False),
                                    "you_learn": my_l.to_dict(include_owner=False),
                                    "match_type": "mutual_exchange"
                                })
                                found_exchange = True
                                break
                        if found_exchange:
                            break
                if found_exchange:
                    break

        # Check for one-way mentor matches (they teach what I want to learn)
        for my_l in my_learns:
            for their_t in other_teaches:
                if _is_match(my_l.skill_name, their_t.skill_name):
                    mentor_matches.append({
                        "mentor": other_user.to_dict(),
                        "skill_offered": their_t.to_dict(include_owner=False),
                        "your_interest": my_l.to_dict(include_owner=False),
                        "match_type": "mentor_available"
                    })

        # Check for one-way learner matches (they want to learn what I teach)
        for my_t in my_teaches:
            for their_l in other_learns:
                if _is_match(my_t.skill_name, their_l.skill_name):
                    learner_matches.append({
                        "learner": other_user.to_dict(),
                        "skill_wanted": their_l.to_dict(include_owner=False),
                        "your_offering": my_t.to_dict(include_owner=False),
                        "match_type": "learner_available"
                    })

    return jsonify({
        "exchange_matches": exchange_matches,
        "total_exchange_matches": len(exchange_matches),
        "mentor_matches": mentor_matches,
        "total_mentor_matches": len(mentor_matches),
        "learner_matches": learner_matches,
        "total_learner_matches": len(learner_matches)
    }), 200
