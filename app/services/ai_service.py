import google.generativeai as genai
from flask import current_app


def _get_model():
    """Configure and return a Gemini model, or None if no API key is set."""
    api_key = current_app.config["GOOGLE_AI_API_KEY"]
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash")


def generate_invitation_message(guest_name: str, group: str, bride: str,
                                 groom: str, date: str, venue: str) -> str:
    """Generate a personalized Hebrew invitation message via Gemini."""
    model = _get_model()

    if not model:
        # Fallback template — works without any API key
        return (
            f"שלום {guest_name} 💍\n"
            f"אנחנו שמחים להזמינך לחגוג איתנו את חתונתנו!\n"
            f"👰 {bride} & 🤵 {groom}\n"
            f"📅 {date}\n"
            f"📍 {venue}\n"
            f"מחכים לראותך! ❤️"
        )

    tone = {
        "family": "חם ואישי מאוד, כמו לבן משפחה קרוב",
        "friends": "קליל ושמח, עם הומור קל",
        "work": "מכובד אך ידידותי",
    }.get(group or "friends", "ידידותי")

    prompt = (
        f"אתה עוזר שכותב הזמנות לחתונה בעברית. "
        f"הסגנון שלך: {tone}. "
        f"כתוב הודעת וואטסאפ קצרה ומרגשת, עד 5 שורות, עם אימוג'ים מתאימים.\n\n"
        f"כתוב הזמנה לחתונה עבור {guest_name}.\n"
        f"החתן: {groom}, הכלה: {bride}\n"
        f"תאריך: {date}\n"
        f"מקום: {venue}"
    )

    response = model.generate_content(prompt)
    return response.text.strip()


def generate_reminder_message(guest_name: str, bride: str, groom: str,
                               date: str, venue: str, days_left: int) -> str:
    """Generate a personalized Hebrew reminder message via Gemini."""
    model = _get_model()

    if not model:
        return (
            f"היי {guest_name}! 👋\n"
            f"תזכורת: החתונה של {bride} & {groom} בעוד {days_left} ימים!\n"
            f"📅 {date} | 📍 {venue}\n"
            f"מחכים לראותך! 🎉"
        )

    prompt = (
        f"כתוב תזכורת לחתונה בעברית, קצרה ומשמחת, עד 4 שורות, עם אימוג'ים.\n"
        f"תזכורת עבור {guest_name}: "
        f"חתונת {bride} ו-{groom} בעוד {days_left} ימים. "
        f"תאריך: {date}, מקום: {venue}"
    )

    response = model.generate_content(prompt)
    return response.text.strip()
