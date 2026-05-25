from datetime import datetime
from app import db


class Guest(db.Model):
    __tablename__ = "guests"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    group_name = db.Column(db.String(50))  # family, friends, work, etc.
    invitation_sent = db.Column(db.Boolean, default=False)
    invitation_sent_at = db.Column(db.DateTime)
    reminder_sent = db.Column(db.Boolean, default=False)
    reminder_sent_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    logs = db.relationship("MessageLog", backref="guest", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "group_name": self.group_name,
            "invitation_sent": self.invitation_sent,
            "invitation_sent_at": (
                self.invitation_sent_at.isoformat()
                if self.invitation_sent_at
                else None
            ),
            "reminder_sent": self.reminder_sent,
            "reminder_sent_at": (
                self.reminder_sent_at.isoformat() if self.reminder_sent_at else None
            ),
            "notes": self.notes,
        }
