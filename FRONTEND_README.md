# SmartLab Hub — Frontend Documentation

A complete web-based frontend for the SmartLab Hub scientific equipment management platform. Built as Django-served HTML/CSS/JS templates connected to the existing REST API backend.

## 🗄️ Database Change: PostgreSQL → SQLite

Settings updated automatically. The new config uses SQLite (`db.sqlite3` in the project root) — no additional setup required. To revert to PostgreSQL, restore the `DATABASE_URL` environment variable in `SmartLab_Hub/settings.py`.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install django djangorestframework django-filter djangorestframework-simplejwt django-environ django-cors-headers Pillow

# 2. Run migrations (creates db.sqlite3)
python manage.py migrate

# 3. Seed sample data
python seed_data.py

# 4. Collect static files
python manage.py collectstatic --noinput

# 5. Start the server
python manage.py runserver

# Or use the start script:
bash start.sh
```

Open **http://127.0.0.1:8000**

---

## 📁 Templates Folder Structure

```
smartlab_hub/
├── templates/               ← All HTML templates
│   ├── base.html            ← Shared layout (header, sidebar, nav)
│   ├── index.html           ← Landing page
│   ├── auth.html            ← Login & Register (combined)
│   ├── dashboard.html       ← Student/Researcher dashboard
│   ├── equipment.html       ← Equipment catalog + booking modal
│   ├── bookings.html        ← My bookings (reused for vendor too)
│   ├── feedback.html        ← Reviews & incident reports
│   ├── profile.html         ← User profile & settings
│   ├── vendor_dashboard.html    ← Vendor overview & analytics
│   ├── vendor_equipment.html    ← Vendor equipment management
│   ├── vendor_inventory.html    ← Physical unit tracker
│   └── admin_dashboard.html     ← Admin analytics & management
│
└── templates/static/        ← Frontend static files
    ├── css/
    │   └── smartlab.css     ← Complete design system
    └── js/
        └── smartlab.js      ← API client, utilities, charts
```

---

## 🌐 Frontend Pages & Routes

| URL | Template | Role |
|-----|----------|------|
| `/` | `index.html` | Public |
| `/login` | `auth.html` | Public |
| `/register` | `auth.html` | Public |
| `/dashboard` | `dashboard.html` | Student / Researcher |
| `/equipment` | `equipment.html` | All authenticated |
| `/bookings` | `bookings.html` | All authenticated |
| `/feedback` | `feedback.html` | All authenticated |
| `/profile` | `profile.html` | All authenticated |
| `/vendor/dashboard` | `vendor_dashboard.html` | Vendor |
| `/vendor/equipment` | `vendor_equipment.html` | Vendor |
| `/vendor/inventory` | `vendor_inventory.html` | Vendor |
| `/vendor/bookings` | `bookings.html` | Vendor |
| `/admin-dashboard` | `admin_dashboard.html` | Admin / Staff |

---

## 🔑 Demo Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Vendor | `vendor1` | `vendor123` |
| Vendor | `vendor2` | `vendor123` |
| Student | `student1` | `student123` |
| Researcher | `researcher1` | `student123` |

---

## 🏗️ Architecture

### API Client (`smartlab.js`)
`window.API` — a singleton that wraps all backend calls:
- Handles JWT tokens (access + refresh) via `localStorage`
- Auto-refreshes expired tokens
- Role-based redirects after login

### Design System (`smartlab.css`)
- **Dark theme** with blue (`#3b9eff`) and green (`#00e5a0`) accents
- **CSS variables** for theming consistency
- **Fonts**: Syne (display) + DM Sans (body)
- Responsive grid layouts, stat cards, tables, modals, toasts

### Role-Based Navigation
`base.html` reads the user's role from `localStorage` and shows/hides sidebar sections:
- `STUDENT` / `RESEARCHER` → student nav only
- `VENDOR` → student nav + vendor nav section
- `ADMIN` / `is_staff` → all sections including admin

---

## 📊 Dashboard Features

### Student Dashboard (`/dashboard`)
- Active/completed/pending/overdue booking counts
- Recent bookings table
- Upcoming return dates
- Available equipment preview
- Monthly booking bar chart

### Vendor Dashboard (`/vendor/dashboard`)
- Revenue metrics (total KES)
- Fleet status donut chart (available/rented/maintenance/damaged)
- Recent booking requests
- Monthly revenue bar chart
- Top-performing equipment
- Pending check-in list

### Admin Dashboard (`/admin-dashboard`)
- Fleet health % and donut chart
- Total revenue, users, bookings, vendors
- Incident type bar chart
- High-risk student list (2+ incidents)
- Pending vendor approvals with one-click approve
- Full user management table with role filter
- All incidents table
- Bookings-by-status donut chart
- Revenue trend chart

---

## 🔌 API Endpoints Used

All calls go to `/api/…` on the same Django server:

```
POST   /api/auth/login/              — JWT login
POST   /api/auth/token/refresh/      — Token refresh
POST   /api/users/register/          — Registration
GET    /api/users/profile/me/        — My profile
PATCH  /api/users/profile/me/        — Update profile
GET    /api/users/list/              — All users (admin)
POST   /api/users/approve-vendor/{id}/ — Approve vendor
GET    /api/catalog/equipment/       — Browse equipment
GET/POST/PATCH/DELETE /api/catalog/manage/ — Vendor CRUD
GET    /api/inventory/               — List units
POST   /api/inventory/{id}/check_in/ — Check-in equipment
GET    /api/bookings/                — My bookings
POST   /api/bookings/                — Create booking
GET    /api/feedback/reviews/        — Equipment reviews
POST   /api/feedback/reviews/        — Submit review
GET    /api/feedback/incidents/      — Incident reports
POST   /api/feedback/incidents/      — Report incident
GET    /api/analysis/dashboard/      — Admin analytics
```

---

## 💳 Payment Flow

1. User creates a booking → Django calls Paystack `initialize`
2. Backend returns `checkout_url` → frontend redirects user to Paystack
3. Paystack calls `/api/payments/callback/` on completion
4. Booking status updated to `CONFIRMED`
