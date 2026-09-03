from datetime import datetime
import bcrypt
from extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())

    # Relationships
    skills = db.relationship(
        "Skill",
        backref="owner",
        lazy="dynamic",
        cascade="all, delete-orphan",
        foreign_keys="Skill.user_id"
    )
    sent_requests = db.relationship(
        "SkillRequest",
        backref="requester",
        lazy="dynamic",
        cascade="all, delete-orphan",
        foreign_keys="SkillRequest.requester_id"
    )
    teaching_sessions = db.relationship(
        "LearningSession",
        backref="teacher",
        lazy="dynamic",
        foreign_keys="LearningSession.teacher_id"
    )
    learning_sessions = db.relationship(
        "LearningSession",
        backref="learner",
        lazy="dynamic",
        foreign_keys="LearningSession.learner_id"
    )

    def set_password(self, plain_password: str) -> None:
        """Hashes password using bcrypt with salt."""
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")

    def check_password(self, plain_password: str) -> bool:
        """Verifies candidate password against stored bcrypt hash."""
        if not self.password or not plain_password:
            return False
        try:
            return bcrypt.checkpw(
                plain_password.encode("utf-8"),
                self.password.encode("utf-8")
            )
        except Exception:
            return False

    def to_dict(self, include_email: bool = True) -> dict:
        """Serializes user model to dictionary without exposing password hash."""
        data = {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        if include_email:
            data["email"] = self.email
        return data

    def __repr__(self) -> str:
        return f"<User id={self.id} email='{self.email}'>"
