import os
import sys
from flask import Flask, jsonify
from sqlalchemy import text

# Ensure backend directory is in the import path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from extensions import db, cors
from routes import auth_bp, skills_bp, requests_bp, matches_bp, sessions_bp


def create_app(config_class=Config):
    """Application factory for SkillBridge backend."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    db.init_app(app)

    # ---------------------------------------------------------
    # Register API Blueprints
    # ---------------------------------------------------------
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(skills_bp, url_prefix="/api/skills")
    app.register_blueprint(requests_bp, url_prefix="/api/requests")
    app.register_blueprint(matches_bp, url_prefix="/api/matches")
    app.register_blueprint(sessions_bp, url_prefix="/api/sessions")

    # ---------------------------------------------------------
    # Core Health & Base Endpoints
    # ---------------------------------------------------------
    @app.route("/api/hello", methods=["GET"])
    def hello():
        """Welcome route (preserved from original codebase)."""
        return jsonify({
            "message": "Welcome to SkillBridge API!"
        })

    @app.route("/api/db-health", methods=["GET"])
    def db_health():
        """
        Database health verification endpoint.
        Safely tests MySQL connectivity without leaking credentials or secrets.
        """
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify({
                "status": "healthy",
                "database": "connected",
                "message": "Successfully connected to MySQL database."
            }), 200
        except Exception:
            # Mask internal connection details and raw database errors for security
            return jsonify({
                "status": "unhealthy",
                "database": "disconnected",
                "message": "Database connection could not be established. Please verify credentials in your .env file."
            }), 503

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)