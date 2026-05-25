#!/bin/bash
set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo "💍  Wedding Invite Manager — Quick Start"
echo "────────────────────────────────────────"

# 1. Docker check
if ! command -v docker &> /dev/null; then
  echo -e "${RED}✗ Docker לא מותקן.${NC}"
  echo "  הורד מ: https://docs.docker.com/get-docker/"
  exit 1
fi

if ! docker info &> /dev/null; then
  echo -e "${RED}✗ Docker לא פועל. הפעל את Docker Desktop ונסה שוב.${NC}"
  exit 1
fi

echo -e "${GREEN}✓ Docker פועל${NC}"

# 2. .env check
if [ ! -f .env ]; then
  cp .env.example .env
  echo -e "${YELLOW}⚠  נוצר קובץ .env מהדוגמה.${NC}"
  echo -e "${YELLOW}   ערוך אותו עם ה-API keys שלך לפני שליחת הודעות אמיתיות.${NC}"
  echo -e "${YELLOW}   (האפליקציה עובדת גם ללא keys — במצב demo)${NC}"
fi

echo -e "${GREEN}✓ קובץ .env קיים${NC}"

# 3. Build & run
echo ""
echo "▶  מריץ docker-compose..."
docker compose up -d --build

# 4. Wait for health
echo ""
echo -n "⏳ ממתין לעלייה של MySQL"
for i in {1..30}; do
  if docker compose exec -T mysql mysqladmin ping -h localhost -u root -proot_password &>/dev/null 2>&1; then
    echo -e " ${GREEN}✓${NC}"
    break
  fi
  echo -n "."
  sleep 2
done

# 5. Print URLs
echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅  המערכת פעילה!${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "  🌐  אפליקציה:  http://localhost"
echo "  📊  Grafana:   http://localhost:3000  (admin / admin123)"
echo "  🔭  Prometheus: http://localhost:9090"
echo ""
echo "  כדי לעצור:  docker compose down"
echo "  לוגים:      docker compose logs -f app"
echo ""
