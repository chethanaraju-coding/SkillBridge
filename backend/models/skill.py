from datetime import datetime
from extensions import db


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False, index=True)
    skill_type = db.Column(db.String(50), nullable=False)  # 'teach' or 'learn'
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())

    # Relationships
    requests = db.relationship(
        "SkillRequest",
        backref="skill",
        lazy="dynamic",
        cascade="all, delete-orphan",
        foreign_keys="SkillRequest.skill_id"
    )
    sessions = db.relationship(
        "LearningSession",
        backref="skill",
        lazy="dynamic",
        foreign_keys="LearningSession.skill_id"
    )

    def to_dict(self, include_owner: bool = True) -> dict:
        """Serializes skill model to dictionary."""
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "skill_name": self.skill_name,
            "skill_type": self.skill_type,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        if include_owner and self.owner:
            data["owner_name"] = self.owner.name
        return data

    def __repr__(self) -> str:
        return f"<Skill id={self.id} name='{self.skill_name}' type='{self.skill_type}'>"
