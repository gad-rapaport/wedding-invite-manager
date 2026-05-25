from flask import current_app
from openai import OpenAI


def generate_invitation_message(guest_name: str, group: str, bride: str, groom: str,
                                 date: str, venue: str) -> str:
    """Use OpenAI to generate a personalized invitation message in Hebrew."""
    api_key = current_app.config["OPENAI_API_KEY"]

    if not api_key:
        # Fallback template when no API key is configured
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

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "אתה עוזר שכותב הזמנות לחתונה בעברית. "
                    f"הסגנון שלך: {tone}. "
                    "כתוב הודעת וואטסאפ קצרה ומרגשת, עד 5 שורות, עם אימוג'ים מתאימים."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"כתוב הזמנה לחתונה עבור {guest_name}.\n"
                    f"החתן: {groom}, הכלה: {bride}\n"
                    f"תאריך: {date}\n"
                    f"מקום: {venue}"
                ),
            },
        ],
        max_tokens=200,
        temperature=0.8,
    )
    return response.choices[0].message.content.strip()


def generate_reminder_message(guest_name: str, bride: str, groom: str,
                               date: str, venue: str, days_left: int) -> str:
    """Generate a personalized reminder message."""
    api_key = current_app.config["OPENAI_API_KEY"]

    if not api_key:
        return (
            f"היי {guest_name}! 👋\n"
            f"תזכורת: החתונה של {bride} & {groom} בעוד {days_left} ימים!\n"
            f"📅 {date} | 📍 {venue}\n"
            f"מחכים לראותך! 🎉"
        )

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "כתוב תזכורת לחתונה בעברית, קצרה ומשמחת, עד 4 שורות.",
            },
            {
                "role": "user",
                "content": (
                    f"תזכורת עבור {guest_name}: "
                    f"חתונת {bride} ו-{groom} בעוד {days_left} ימים. "
                    f"תאריך: {date}, מקום: {venue}"
                ),
            },
        ],
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
