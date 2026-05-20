#!/bin/bash
# ─────────────────────────────────────────────
#  SmartLab Hub — Quick Start Script
# ─────────────────────────────────────────────

set -e
cd "$(dirname "$0")"

echo ""
echo "╔══════════════════════════════════════╗"
echo "║        SmartLab Hub Startup          ║"
echo "╚══════════════════════════════════════╝"
echo ""

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --run-syncdb

# Seed data only on first run (less than 3 users means fresh DB)
USER_COUNT=$(python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','SmartLab_Hub.settings')
django.setup()
from users.models import User
print(User.objects.count())
" 2>/dev/null || echo "0")

if [ "$USER_COUNT" -lt "3" ]; then
  echo "🌱 Seeding sample data..."
  python seed_data.py
fi

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput -q

echo ""
echo "────────────────────────────────────────"
echo "  ✅  Ready!  Open: http://127.0.0.1:8000"
echo ""
echo "  👤 Admin:       admin / admin123"
echo "  🏪 Vendor:      vendor1 / vendor123"
echo "  🎓 Student:     student1 / student123"
echo "  🔬 Researcher:  researcher1 / student123"
echo "  🔧 Django Admin: http://127.0.0.1:8000/admin"
echo "────────────────────────────────────────"
echo ""

python manage.py runserver 0.0.0.0:8000
