# Wedding Invite Manager - Quick Start (Windows PowerShell)
$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "💍  Wedding Invite Manager — Quick Start" -ForegroundColor Magenta
Write-Host "────────────────────────────────────────" -ForegroundColor DarkGray

# 1. Docker check
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "✗ Docker לא מותקן." -ForegroundColor Red
    Write-Host "  הורד מ: https://docs.docker.com/get-docker/" -ForegroundColor Yellow
    exit 1
}

try {
    docker info 2>&1 | Out-Null
} catch {
    Write-Host "✗ Docker לא פועל. הפעל את Docker Desktop ונסה שוב." -ForegroundColor Red
    exit 1
}

Write-Host "✓ Docker פועל" -ForegroundColor Green

# 2. .env check
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "⚠  נוצר קובץ .env מהדוגמה." -ForegroundColor Yellow
    Write-Host "   ערוך אותו עם ה-API keys שלך לפני שליחת הודעות אמיתיות." -ForegroundColor Yellow
    Write-Host "   (האפליקציה עובדת גם ללא keys — במצב demo)" -ForegroundColor Yellow
}

Write-Host "✓ קובץ .env קיים" -ForegroundColor Green

# 3. Build & run
Write-Host ""
Write-Host "▶  מריץ docker-compose..." -ForegroundColor Cyan
docker compose up -d --build

# 4. Wait for MySQL
Write-Host ""
Write-Host "⏳ ממתין לעלייה של MySQL..." -ForegroundColor Yellow
$ready = $false
for ($i = 0; $i -lt 30; $i++) {
    $result = docker compose exec -T mysql mysqladmin ping -h localhost -u root -proot_password 2>&1
    if ($LASTEXITCODE -eq 0) { $ready = $true; break }
    Start-Sleep -Seconds 2
    Write-Host "  ." -NoNewline
}
if ($ready) { Write-Host " ✓" -ForegroundColor Green }

# 5. Print URLs
Write-Host ""
Write-Host "════════════════════════════════════════" -ForegroundColor Green
Write-Host "  ✅  המערכת פעילה!" -ForegroundColor Green
Write-Host "════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "  🌐  אפליקציה:   http://localhost"
Write-Host "  📊  Grafana:    http://localhost:3000  (admin / admin123)"
Write-Host "  🔭  Prometheus: http://localhost:9090"
Write-Host ""
Write-Host "  כדי לעצור:  docker compose down"
Write-Host "  לוגים:      docker compose logs -f app"
Write-Host ""
