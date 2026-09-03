import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Locate and load the .env file from project root and/or backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(backend_dir)
root_env = os.path.join(root_dir, ".env")
backend_env = os.path.join(backend_dir, ".env")

if os.path.exists(root_env):
    load_dotenv(dotenv_path=root_env, override=True)
if os.path.exists(backend_env):
    load_dotenv(dotenv_path=backend_env, override=True)
load_dotenv()


class Config:
    """Base application configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "skillbridge-dev-secret-key-change-in-production")
    
    # Database Settings
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "skillbridge")

    # Safely encode credentials for MySQL URI
    _encoded_password = quote_plus(DB_PASSWORD) if DB_PASSWORD else ""
    _auth_part = f"{DB_USER}:{_encoded_password}" if _encoded_password else DB_USER

    # Allow full DATABASE_URL override, otherwise construct PyMySQL connection string
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"mysql+pymysql://{_auth_part}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 3600,
    }

    # JWT Settings
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES_HOURS = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", "24"))
