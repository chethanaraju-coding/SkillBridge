from datetime import datetime, timedelta, timezone
from functools import wraps
import jwt
from flask import request, jsonify, current_app
from models.user import User


def _get_jwt_secret() -> str:
    secret = current_app.config.get("JWT_SECRET_KEY") or "skillbridge-default-jwt-secret-key-2026-secure"
    if len(secret) < 32:
        secret = secret.ljust(32, "_")
    return secret


def generate_token(user: User) -> str:
    """
    Generates a secure JWT token containing user identity and expiration.
    """
    secret = _get_jwt_secret()
    expires_hours = current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES_HOURS", 24)
    exp = datetime.now(timezone.utc) + timedelta(hours=expires_hours)

    payload = {
        "user_id": user.id,
        "sub": str(user.id),
        "email": user.email,
        "name": user.name,
        "exp": exp,
        "iat": datetime.now(timezone.utc)
    }

    return jwt.encode(payload, secret, algorithm="HS256")


def decode_token(token: str):
    """
    Decodes and validates a JWT token.
    Returns: (payload, error_message)
    """
    secret = _get_jwt_secret()
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, "Authentication token has expired. Please log in again."
    except jwt.InvalidTokenError:
        return None, "Invalid authentication token. Please log in again."
    except Exception as e:
        return None, "Failed to authenticate token."


def token_required(f):
    """
    Decorator to protect API routes with JWT authentication.
    Injects `current_user` into the route kwargs.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({
                "error": "Authentication required. Missing Authorization header."
            }), 401

        # Format: 'Bearer <token>'
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({
                "error": "Invalid Authorization header format. Expected 'Bearer <token>'."
            }), 401

        token = parts[1]
        payload, error = decode_token(token)
        if error:
            return jsonify({"error": error}), 401

        user_id = payload.get("user_id")
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                "error": "User associated with this token no longer exists."
            }), 401

        return f(*args, current_user=user, **kwargs)

    return decorated
