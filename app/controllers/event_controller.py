from app import db
from app.models.event import Event


def get_active_event():
    return Event.query.first()


def create_or_update_event(data: dict) -> Event:
    event = Event.query.first()
    if not event:
        event = Event()
        db.session.add(event)

    event.bride_name = data.get("bride_name", "")
    event.groom_name = data.get("groom_name", "")

    from datetime import datetime
    wedding_date_str = data.get("wedding_date", "")
    if wedding_date_str:
        event.wedding_date = datetime.strptime(wedding_date_str, "%Y-%m-%dT%H:%M")

    event.venue = data.get("venue", "")
    event.venue_address = data.get("venue_address", "")
    event.custom_message = data.get("custom_message", "")
    event.reminder_days_before = int(data.get("reminder_days_before", 7))

    if data.get("invitation_image_path"):
        event.invitation_image_path = data["invitation_image_path"]

    db.session.commit()
    return event
