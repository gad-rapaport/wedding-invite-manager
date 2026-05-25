import os
from flask import current_app
from twilio.rest import Client


def send_whatsapp_message(to_phone: str, message: str, image_url: str = None) -> dict:
    """Send a WhatsApp message via Twilio. Returns status dict."""
    account_sid = current_app.config["TWILIO_ACCOUNT_SID"]
    auth_token = current_app.config["TWILIO_AUTH_TOKEN"]
    from_number = current_app.config["TWILIO_WHATSAPP_FROM"]

    # In test/dev mode without credentials, simulate sending
    if not account_sid or not auth_token:
        current_app.logger.warning(
            f"[MOCK] WhatsApp to {to_phone}: {message[:60]}..."
        )
        return {"status": "sent", "sid": "MOCK_SID", "mock": True}

    client = Client(account_sid, auth_token)

    params = {
        "from_": from_number,
        "to": f"whatsapp:{to_phone}",
        "body": message,
    }
    if image_url:
        params["media_url"] = [image_url]

    msg = client.messages.create(**params)
    return {"status": msg.status, "sid": msg.sid, "mock": False}


def send_bulk_whatsapp(guests: list, message_builder, image_url: str = None) -> list:
    """Send WhatsApp messages to a list of guests. Returns results list."""
    results = []
    for guest in guests:
        try:
            message = message_builder(guest)
            result = send_whatsapp_message(guest.phone, message, image_url)
            results.append({"guest_id": guest.id, "success": True, **result})
        except Exception as e:
            current_app.logger.error(f"Failed sending to {guest.phone}: {e}")
            results.append({"guest_id": guest.id, "success": False, "error": str(e)})
    return results
