from datetime import datetime
from app import db


class MessageLog(db.Model):
    __tablename__ = "message_logs"

    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.id"), nullable=False)
    message_type = db.Column(db.String(20), nullable=False)  # invitation / reminder
    status = db.Column(db.String(20), default="sent")  # sent / failed
    message_body = db.Column(db.Text)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "guest_id": self.guest_id,
            "message_type": self.message_type,
            "status": self.status,
            "message_body": self.message_body,
            "sent_at": self.sent_at.isoformat(),
        }
