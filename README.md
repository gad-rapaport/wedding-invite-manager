# Wedding Invite Manager

מערכת לשליחת הזמנות חתונה ב-WhatsApp בכמויות גדולות, עם הודעות מותאמות אישית באמצעות בינה מלאכותית (Google Gemini) ותזכורות אוטומטיות.

---

## ארכיטקטורה

```
Browser → Nginx (8080) → Flask/Gunicorn (5000) → MySQL
                                ↓
                     Green API (WhatsApp)
                     Google Gemini AI
                                ↑
Prometheus (9090) ← /metrics endpoint
Grafana    (3000) ← Prometheus
```

### שכבות המערכת

| שכבה | טכנולוגיה | תפקיד |
|------|-----------|-------|
| Frontend / Proxy | Nginx | Reverse proxy, static files, הגנת סף |
| Backend | Flask + Gunicorn | לוגיקה עסקית, REST API |
| Database | MySQL 8 | אחסון אורחים, אירועים, לוגים |
| AI | Google Gemini 2.0 Flash | יצירת הודעות אישיות בעברית |
| WhatsApp | Green API | שליחת הודעות WhatsApp אמיתיות |
| Monitoring | Prometheus + Grafana | מדדים ולוחות בקרה |
| Containerization | Docker + Docker Compose | אריזה והרצה |
| CI/CD | GitHub Actions | בדיקות → build → push → deploy |
| IaC | Terraform | הקמת EC2 + Security Group ב-AWS |

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

הסקריפט:
1. בודק שDocker פועל
2. יוצר קובץ `.env` אוטומטית
3. בונה ומעלה את כל המערכת
4. מדפיס את הכתובות

---

## כתובות אחרי ההפעלה

| שירות | כתובת |
|-------|--------|
| אפליקציה | http://localhost:8080 |
| Grafana (ניטור) | http://localhost:3000 |
| Prometheus | http://localhost:9090 |

Grafana: משתמש `admin` / סיסמה `admin123`

---

## הגדרת API Keys (אופציונלי)

האפליקציה **עובדת גם ללא keys** — במצב mock, הודעות מודפסות ללוג במקום לשלוח.

לשליחה אמיתית — ערוך את קובץ `.env` שנוצר אוטומטית:

```env
# Green API (WhatsApp) — app.green-api.com
GREEN_API_INSTANCE_ID=your_instance_id
GREEN_API_TOKEN=your_token

# Google AI (Gemini) — aistudio.google.com
GOOGLE_AI_API_KEY=AIzaxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
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

## CI/CD Pipeline (GitHub Actions)

```
git push → main
    │
    ├─ Stage 1: pytest (SQLite in-memory)
    │       └─ fail → email לצוות
    │
    ├─ Stage 2: docker build + push to Docker Hub
    │       (tagged: latest + SHA)
    │
    └─ Stage 3: SSH לHetzner → git pull + docker-compose up -d
```

### Secrets הנדרשים ב-GitHub

| Secret | תיאור |
|--------|-------|
| `DOCKER_USERNAME` | שם משתמש Docker Hub |
| `DOCKER_PASSWORD` | סיסמת Docker Hub |
| `SERVER_HOST` | כתובת IP של שרת Hetzner |
| `SERVER_SSH_KEY` | מפתח SSH פרטי |
| `MAIL_USERNAME` | כתובת Gmail לשליחת התראות |
| `MAIL_PASSWORD` | App Password של Gmail |
| `MAIL_TO` | כתובת יעד לקבלת התראות |

---

## פריסה בענן — Hetzner Cloud עם Terraform

```bash
cd terraform

terraform init
terraform apply \
  -var="hcloud_token=YOUR_HETZNER_API_TOKEN" \
  -var="ssh_public_key=$(cat ~/.ssh/id_rsa.pub)" \
  -var="github_repo=user/wedding-invite-manager" \
  -var="secret_key=strong-secret" \
  -var="green_api_instance_id=XXXXX" \
  -var="green_api_token=YYYYY" \
  -var="google_ai_key=AIza..."
```

Terraform מקים:
- Hetzner CX22 (2 vCPU / 4 GB RAM) עם Ubuntu 22.04
- Firewall (ports 22, 80, 3000)
- SSH Key
- Bash user-data script שמתקין Docker ומעלה את האפליקציה על פורט 80 אוטומטית

> **פורט:** בשרת Hetzner האפליקציה רצה על פורט **80** (מוגדר דרך `NGINX_PORT=80` ב-.env).
> בסביבה מקומית: `http://localhost:8080` (ברירת מחדל ללא NGINX_PORT).

---

## מבנה הפרויקט

```
wedding-invite-manager/
├── app/
│   ├── __init__.py          # Flask app factory + DB + Prometheus
│   ├── config.py            # הגדרות מסביבה
│   ├── models/              # Guest, Event, MessageLog (SQLAlchemy)
│   ├── controllers/         # לוגיקה עסקית
│   ├── routes/              # api_routes.py + ui_routes.py
│   ├── services/            # whatsapp_service.py + ai_service.py
│   └── templates/           # Jinja2 HTML
├── tests/
│   ├── conftest.py          # pytest fixtures (SQLite in-memory)
│   └── test_api.py          # בדיקות CRUD + health
├── nginx/nginx.conf         # Reverse proxy config
├── monitoring/prometheus.yml
├── terraform/               # main.tf + variables.tf + outputs.tf
├── .github/workflows/ci.yml # CI/CD pipeline
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## שינויים אחרונים

### גרסה נוכחית — Hetzner
- **Green API במקום Twilio** — עבר ל-Green API לשליחת WhatsApp אמיתית בישראל; פורמט הטלפון מותאם (05x → 9725x@c.us)
- **Google Gemini במקום OpenAI** — מודל `gemini-2.0-flash` ליצירת הודעות עברית אישיות
- **Nginx על פורט 8080** — בסביבת dev המקומית; בEC2 רץ על פורט 80 ישירות
- **תיקון Terraform** — משתני `twilio_*` הוחלפו ב-`green_api_instance_id` ו-`green_api_token`
- **תיקון conftest.py** — TEST_CONFIG מכיל את המשתנים הנכונים (GREEN_API / GOOGLE_AI)
- **CI שולח email על כישלון** — via dawidd6/action-send-mail עם Gmail SMTP
- **מעבר מ-AWS EC2 ל-Hetzner Cloud** — Terraform עם `hcloud` provider; שרת `cx22` Ubuntu 22.04; SSH user: `root`; secrets שונו מ-`EC2_HOST/EC2_SSH_KEY` ל-`SERVER_HOST/SERVER_SSH_KEY`
- **פורט Nginx דינמי** — `${NGINX_PORT:-8080}:80`; הגדר `NGINX_PORT=80` ב-.env בשרת להפעלה על פורט 80
