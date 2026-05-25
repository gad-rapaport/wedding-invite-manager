from datetime import datetime
from app import db
from app.models.guest import Guest
from app.models.message_log import MessageLog
from app.services import whatsapp_service, ai_service
from app.controllers.event_controller import get_active_event


def get_all_guests(group_filter=None, status_filter=None, sort_by="name"):
    query = Guest.query
    if group_filter:
        query = query.filter_by(group_name=group_filter)
    if status_filter == "invited":
        query = query.filter_by(invitation_sent=True)
    elif status_filter == "not_invited":
        query = query.filter_by(invitation_sent=False)
    elif status_filter == "reminded":
        query = query.filter_by(reminder_sent=True)
    if sort_by == "name":
        query = query.order_by(Guest.name)
    elif sort_by == "group":
        query = query.order_by(Guest.group_name)
    elif sort_by == "created":
        query = query.order_by(Guest.created_at.desc())
    return query.all()


def get_guest_by_id(guest_id):
    return Guest.query.get_or_404(guest_id)


def create_guest(data: dict) -> Guest:
    guest = Guest(
        name=data["name"],
        phone=data["phone"],
        group_name=data.get("group_name", "friends"),
        notes=data.get("notes", ""),
    )
    db.session.add(guest)
    db.session.commit()
    return guest


def update_guest(guest_id: int, data: dict) -> Guest:
    guest = get_guest_by_id(guest_id)
    guest.name = data.get("name", guest.name)
    guest.phone = data.get("phone", guest.phone)
    guest.group_name = data.get("group_name", guest.group_name)
    guest.notes = data.get("notes", guest.notes)
    db.session.commit()
    return guest


def delete_guest(guest_id: int):
    guest = get_guest_by_id(guest_id)
    db.session.delete(guest)
    db.session.commit()


def send_invitations(guest_ids: list = None) -> dict:
    """Send WhatsApp invitations to selected guests (or all uninvited)."""
    event = get_active_event()
    if not event:
        return {"error": "No event configured"}

    if guest_ids:
        guests = Guest.query.filter(Guest.id.in_(guest_ids)).all()
    else:
        guests = Guest.query.filter_by(invitation_sent=False).all()

    image_url = None
    if event.invitation_image_path:
        image_url = event.invitation_image_path  # public URL or None

    def build_message(guest):
        return ai_service.generate_invitation_message(
            guest_name=guest.name,
            group=guest.group_name,
            bride=event.bride_name,
            groom=event.groom_name,
            date=event.wedding_date.strftime("%d/%m/%Y %H:%M"),
            venue=event.venue or "",
        )

    results = whatsapp_service.send_bulk_whatsapp(guests, build_message, image_url)

    for result in results:
        guest = Guest.query.get(result["guest_id"])
        if result["success"]:
            guest.invitation_sent = True
            guest.invitation_sent_at = datetime.utcnow()
            log = MessageLog(
                guest_id=guest.id,
                message_type="invitation",
                status="sent",
                message_body=result.get("sid", ""),
            )
            db.session.add(log)
        else:
            log = MessageLog(
                guest_id=guest.id,
                message_type="invitation",
                status="failed",
                message_body=result.get("error", ""),
            )
            db.session.add(log)

    db.session.commit()
    sent = sum(1 for r in results if r["success"])
    return {"sent": sent, "failed": len(results) - sent, "total": len(results)}


def send_reminders(guest_ids: list = None) -> dict:
    """Send reminder messages to guests who haven't received one yet."""
    event = get_active_event()
    if not event:
        return {"error": "No event configured"}

    days_left = (event.wedding_date - datetime.utcnow()).days

    if guest_ids:
        guests = Guest.query.filter(Guest.id.in_(guest_ids)).all()
    else:
        guests = Guest.query.filter_by(invitation_sent=True, reminder_sent=False).all()

    def build_reminder(guest):
        return ai_service.generate_reminder_message(
            guest_name=guest.name,
            bride=event.bride_name,
            groom=event.groom_name,
            date=event.wedding_date.strftime("%d/%m/%Y %H:%M"),
            venue=event.venue or "",
            days_left=days_left,
        )

    results = whatsapp_service.send_bulk_whatsapp(guests, build_reminder)

    for result in results:
        guest = Guest.query.get(result["guest_id"])
        if result["success"]:
            guest.reminder_sent = True
            guest.reminder_sent_at = datetime.utcnow()
            log = MessageLog(
                guest_id=guest.id,
                message_type="reminder",
                status="sent",
            )
            db.session.add(log)

    db.session.commit()
    sent = sum(1 for r in results if r["success"])
    return {"sent": sent, "failed": len(results) - sent, "total": len(results)}
