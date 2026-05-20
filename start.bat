@echo off
echo.
echo ╔══════════════════════════════════════╗
echo ║        SmartLab Hub Startup          ║
echo ╚══════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 📦 Installing dependencies...
pip install -q -r requirements.txt

echo 🗄️  Running database migrations...
python manage.py migrate --run-syncdb

echo 🌱 Seeding sample data (first run)...
python seed_data.py

echo 📁 Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ────────────────────────────────────────
echo   Ready!  Open: http://127.0.0.1:8000
echo.
echo   Admin:      admin / admin123
echo   Vendor:     vendor1 / vendor123
echo   Student:    student1 / student123
echo ────────────────────────────────────────
echo.

python manage.py runserver 0.0.0.0:8000
