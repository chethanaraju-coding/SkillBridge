import re
from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from utils.auth import generate_token, token_required

auth_bp = Blueprint("auth", __name__)

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Registers a new user, hashes password with bcrypt, and issues a JWT token.
    """
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    # Validation
    if not name:
        return jsonify({"error": "Full name is required."}), 400
    if len(name) < 2 or len(name) > 100:
        return jsonify({"error": "Name must be between 2 and 100 characters."}), 400

    if not email:
        return jsonify({"error": "Email address is required."}), 400
    if not EMAIL_REGEX.match(email) or len(email) > 150:
        return jsonify({"error": "Please provide a valid email address."}), 400

    if not password:
        return jsonify({"error": "Password is required."}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters long."}), 400

    # Duplicate check
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "An account with this email already exists."}), 409

    try:
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        token = generate_token(user)

        return jsonify({
            "message": "Registration successful!",
            "user": user.to_dict(),
            "token": token
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to register user. Please try again."}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticates user credentials and issues a JWT token.
    """
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are both required."}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password."}), 401

    token = generate_token(user)

    return jsonify({
        "message": "Login successful!",
        "user": user.to_dict(),
        "token": token
    }), 200


@auth_bp.route("/me", methods=["GET"])
@token_required
def get_current_user(current_user):
    """
    Returns the profile of the currently authenticated user.
    """
    return jsonify({
        "user": current_user.to_dict()
    }), 200
