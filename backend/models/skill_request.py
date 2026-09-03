from datetime import datetime
from extensions import db


class SkillRequest(db.Model):
    __tablename__ = "skill_requests"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    requester_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="pending")  # 'pending', 'accepted', 'rejected', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())

    def to_dict(self) -> dict:
        """Serializes skill request model to dictionary."""
        data = {
            "id": self.id,
            "requester_id": self.requester_id,
            "skill_id": self.skill_id,
            "message": self.message,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        if self.requester:
            data["requester_name"] = self.requester.name
        if self.skill:
            data["skill_name"] = self.skill.skill_name
            data["skill_type"] = self.skill.skill_type
            if self.skill.owner:
                data["receiver_id"] = self.skill.owner.id
                data["receiver_name"] = self.skill.owner.name
        return data

    def __repr__(self) -> str:
        return f"<SkillRequest id={self.id} status='{self.status}'>"
