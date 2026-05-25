from flask import current_app


def send_whatsapp_message(to_phone: str, message: str, image_url: str = None) -> dict:
    """Log the message (mock mode). Swap this function for any real provider later."""
    current_app.logger.info(
        f"[WhatsApp] → {to_phone} | {message[:80]}{'...' if len(message) > 80 else ''}"
    )
    return {"status": "sent", "sid": "MOCK", "mock": True}


def send_bulk_whatsapp(guests: list, message_builder, image_url: str = None) -> list:
    results = []
    for guest in guests:
        try:
            message = message_builder(guest)
            result = send_whatsapp_message(guest.phone, message, image_url)
            results.append({"guest_id": guest.id, "success": True, **result})
        except Exception as e:
            current_app.logger.error(f"Failed building message for {guest.phone}: {e}")
            results.append({"guest_id": guest.id, "success": False, "error": str(e)})
    return results
