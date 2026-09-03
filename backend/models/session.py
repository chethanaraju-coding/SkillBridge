from datetime import datetime
from extensions import db


class LearningSession(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    learner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.id"), nullable=False)
    session_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=True)
    status = db.Column(db.String(20), default="scheduled")  # 'scheduled', 'completed', 'cancelled'
    meeting_link = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())

    def to_dict(self) -> dict:
        """Serializes learning session model to dictionary."""
        data = {
            "id": self.id,
            "teacher_id": self.teacher_id,
            "learner_id": self.learner_id,
            "skill_id": self.skill_id,
            "session_date": self.session_date.isoformat() if self.session_date else None,
            "start_time": str(self.start_time) if self.start_time else None,
            "end_time": str(self.end_time) if self.end_time else None,
            "status": self.status,
            "meeting_link": self.meeting_link,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        if self.teacher:
            data["teacher_name"] = self.teacher.name
        if self.learner:
            data["learner_name"] = self.learner.name
        if self.skill:
            data["skill_name"] = self.skill.skill_name
        return data

    def __repr__(self) -> str:
        return f"<LearningSession id={self.id} date='{self.session_date}' status='{self.status}'>"


# Alias for compatibility with project naming
Session = LearningSession
