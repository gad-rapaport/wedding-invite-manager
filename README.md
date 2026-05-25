# 💍 Wedding Invite Manager

שליחת הזמנות חתונה ב-WhatsApp בכמויות, עם הודעות מותאמות אישית דרך AI ותזכורות אוטומטיות.

---

## דרישה אחת בלבד: Docker

**הכל רץ בתוך Docker — אין צורך להתקין Python, MySQL, או שום דבר אחר.**

הורד Docker Desktop:
- **Windows / Mac:** https://www.docker.com/products/docker-desktop
- **Linux:** `curl -fsSL https://get.docker.com | sh`

---

## הפעלה — פקודה אחת

### Windows
```powershell
.\start.ps1
```

### Mac / Linux
```bash
chmod +x start.sh && ./start.sh
```

### כל מערכת (עם make)
```bash
make run
```

זה הכל. הסקריפט:
1. בודק שDocker פועל
2. יוצר קובץ `.env` אוטומטית
3. בונה ומעלה את כל המערכת
4. מדפיס את הכתובות

---

## כתובות אחרי ההפעלה

| שירות | כתובת |
|-------|--------|
| 🌐 אפליקציה | http://localhost |
| 📊 Grafana (ניטור) | http://localhost:3000 |
| 🔭 Prometheus | http://localhost:9090 |

Grafana: משתמש `admin` / סיסמה `admin123`

---

## הגדרת API Keys (אופציונלי)

האפליקציה **עובדת גם ללא keys** — במצב demo, הודעות מודפסות ללוג במקום לשלוח.

לשליחה אמיתית — ערוך את קובץ `.env` שנוצר אוטומטית:

```env
# Twilio WhatsApp — console.twilio.com
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

# OpenAI — platform.openai.com
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

אחרי עריכה: `docker compose restart app`

---

## פקודות שימושיות

```bash
# עצור הכל
docker compose down

# צפה בלוגים בזמן אמת
docker compose logs -f app

# הרץ טסטים
make test

# מחק הכל (כולל נתונים)
make clean
```

---

## ארכיטקטורה

```
Browser → Nginx (80) → Flask app (5000) → MySQL
                              ↓
                    Twilio WhatsApp API
                    OpenAI API
                              ↑
Prometheus (9090) ← /metrics endpoint
Grafana (3000)    ← Prometheus
```
