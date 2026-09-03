"""
Routes package for SkillBridge backend.
Exports:
  - auth_bp
  - skills_bp
  - requests_bp
  - matches_bp
  - sessions_bp
"""
from .auth import auth_bp
from .skills import skills_bp
from .requests import requests_bp
from .matches import matches_bp
from .sessions import sessions_bp

__all__ = [
    "auth_bp",
    "skills_bp",
    "requests_bp",
    "matches_bp",
    "sessions_bp"
]
