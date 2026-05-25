from app import db


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    bride_name = db.Column(db.String(100), nullable=False)
    groom_name = db.Column(db.String(100), nullable=False)
    wedding_date = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String(200))
    venue_address = db.Column(db.Text)
    invitation_image_path = db.Column(db.String(300))
    custom_message = db.Column(db.Text)
    reminder_days_before = db.Column(db.Integer, default=7)

    def to_dict(self):
        return {
            "id": self.id,
            "bride_name": self.bride_name,
            "groom_name": self.groom_name,
            "wedding_date": (
                self.wedding_date.isoformat() if self.wedding_date else None
            ),
            "venue": self.venue,
            "venue_address": self.venue_address,
            "invitation_image_path": self.invitation_image_path,
            "custom_message": self.custom_message,
            "reminder_days_before": self.reminder_days_before,
        }
