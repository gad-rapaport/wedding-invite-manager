import requests
from flask import current_app


def _format_phone(phone: str) -> str:
    """Convert any Israeli format → 972XXXXXXXXX@c.us (Green API format).
    Handles: +972..., 972..., 05...
    """
    cleaned = phone.strip().replace("+", "").replace("-", "").replace(" ", "")
    if cleaned.startswith("0"):
        cleaned = "972" + cleaned[1:]  # 052... → 97252...
    return f"{cleaned}@c.us"


def send_whatsapp_message(to_phone: str, message: str, image_url: str = None) -> dict:
    instance_id = current_app.config.get("GREEN_API_INSTANCE_ID", "")
    token = current_app.config.get("GREEN_API_TOKEN", "")

    if not instance_id or not token:
        # Mock mode — log only
        current_app.logger.info(
            f"[WhatsApp MOCK] → {to_phone}: {message[:80]}"
        )
        return {"status": "sent", "sid": "MOCK", "mock": True}

    base = f"https://api.green-api.com/waInstance{instance_id}"
    chat_id = _format_phone(to_phone)

    try:
        if image_url:
            # Send image with caption
            resp = requests.post(
                f"{base}/sendFileByUrl/{token}",
                json={
                    "chatId": chat_id,
                    "urlFile": image_url,
                    "fileName": "invitation.jpg",
                    "caption": message,
                },
                timeout=15,
            )
        else:
            # Send text only
            resp = requests.post(
                f"{base}/sendMessage/{token}",
                json={"chatId": chat_id, "message": message},
                timeout=15,
            )

        resp.raise_for_status()
        data = resp.json()
        return {"status": "sent", "sid": data.get("idMessage", ""), "mock": False}

    except Exception as e:
        raise RuntimeError(str(e))


def send_bulk_whatsapp(guests: list, message_builder, image_url: str = None) -> list:
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
