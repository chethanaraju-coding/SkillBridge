"""
Extensions module for SkillBridge.
Initializes Flask extensions to prevent circular dependencies.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
cors = CORS()
