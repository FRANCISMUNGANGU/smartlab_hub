# SmartLab Hub Backend API Documentation

```
git clone https://github.com/FRANCISMUNGANGU/smartlab_hub.git
```

## Table of Contents
1. [Project Setup](#project-setup)
2. [API Overview](#api-overview)
3. [Authentication](#authentication)
4. [API Endpoints](#api-endpoints)
   - [User Management](#1-user-management)
   - [Catalog (Equipment Listing)](#2-catalog-equipment-listing)
   - [Inventory Management](#3-inventory-management)
   - [Bookings & Reservations](#4-bookings--reservations)
   - [Feedback & Incident Reports](#5-feedback--incident-reports)
   - [Payments](#6-payments)
   - [Notifications](#7-notifications)
   - [Transactions](#8-transactions)
   - [Admin Dashboard](#9-admin-dashboard)

---

## Project Setup

### Before You Start
1. All Python modules listed in `requirements.txt` must be installed
2. Docker and Docker Compose must be installed. Download from https://www.docker.com/get-started/ and follow installation instructions for your OS. Once installed, run docker compose up -d to start the backend and database containers.
3. NGROK is required for local testing of payment callbacks. You can sign up for a free account at https://ngrok.com/ and set up a tunnel to your local backend (e.g., `ngrok http 8000`). Update the `NGROK_URL` variable in your `.env` file with the generated URL (e.g., `https://d012-102-205-238-224.ngrok-free.app`)
4. Paystack API keys are required for payment processing (you can create a free account at https://paystack.com/ and get your test keys. Set them in your `.env` and `PAYSTACK_SECRET_KEY` and ensure to set the callback and webhook URLs in your Paystack dashboard to point to your backend endpoints in Paystack settings ie `https://yourdomain.com/api/payments/callback/` and `https://yourdomain.com/api/payments/webhook/`)
5. Environment variables must be set in `.env` file (database credentials, API keys, etc.)

6. POSTGRESQL DATABASE SETUP:
   - Create a PostgreSQL database named `smartlab_db` (and update `DATABASE_URL` in `.env` to match your database name)
   - Create a database user with appropriate permissions and update the `DATABASE_URL` in `.env` with the correct username and password
   - Run database migrations with `docker compose exec api python manage.py migrate`
   - Create a superuser for admin access with `docker compose exec api python manage.py createsuperuser`

### Important Notes
- All API responses are in **JSON format**
- Use Insomnia or Postman to test endpoints and explore response structures
- The project uses Docker for containerization and Nginx for scalability
- The project uses NGROK for local testing of payment callbacks.
- Authentication is JWT-based (JSON Web Tokens)
- Run: 
```docker compose exec api python manage.py collectstatic --noinput``` after running docker compose up -d or after making changes to static files (e.g., images) to ensure they are served correctly. The static files are served by Nginx in production and must be collected to the correct directory for access. 
- ## THE PROJECT WILL NOT WORK WITHOUT PROPER ENVIRONMENT VARIABLES, DOCKER AND NGROK SETUP FOR PAYMENTS. PLEASE FOLLOW THE SETUP INSTRUCTIONS CAREFULLY. DO NOT IGNORE THESE INSTRUCTIONS. ##

---

## API Overview

**Base URL:** `http://localhost:8000/api/`

## Base URL Configuration

- **Development (local):** `http://localhost:8000/api/`
- **Docker/Nginx (local):** `http://localhost/api/`
- **Production:** `https://yourdomain.com/api/`

Configure your frontend `.env` file:
```env
REACT_APP_API_BASE_URL=http://localhost:8000/api/  # Development
# or
REACT_APP_API_BASE_URL=http://localhost/api/       # Docker local
# or
REACT_APP_API_BASE_URL=https://api.yourdomain.com/api/  # Production

**Default Response Format:**
Most API endpoints return direct DRF serializer data or custom DRF payloads. Some endpoints may return additional metadata, such as:
```json
{
  "message": "User registered successfully",
  "user": { /* user object */ }
}
```

**Health Check:**
- `GET /` → Returns API status and service information

---

## Authentication

### 1. User Registration
**Endpoint:** `POST /api/users/register/`

**Required Input:**
```json
{
  "username": "string (unique)",
  "email": "string (unique)",
  "password": "string",
  "first_name": "string",
  "last_name": "string",
  "role": "STUDENT | RESEARCHER | VENDOR",
  "phone": "string (optional)",
  "organization": "string (optional)",
  "profile_picture": "file (optional)"
}
```

**Expected Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "STUDENT",
    "phone": "254712345678",
    "organization": "University of Nairobi",
    "profile_picture": null
  }
}
```

### 2. User Login (Get JWT Token)
**Endpoint:** `POST /api/auth/login/`

**Required Input:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Expected Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**How to Use Token:**
- Add `Authorization: Bearer <access_token>` header to all authenticated requests
- When access token expires, use refresh token to get a new one

### 3. Refresh JWT Token
**Endpoint:** `POST /api/auth/token/refresh/`

**Required Input:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Expected Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## API Endpoints

### 1. User Management

#### Get Current User Profile
**Endpoint:** `GET /api/users/profile/me/`


**Required:** Authentication (JWT Token)

**Expected Response (200 OK):**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "STUDENT",
  "phone": "254712345678",
  "organization": "University of Nairobi",
  "profile_picture": "https://api.example.com/profile_pictures/john_doe.jpg"
}
```

#### Update User Profile
**Endpoint:** `PUT/PATCH /api/users/profile/me/`

**Required:** Authentication (JWT Token)

**Input (all fields optional):**
```json
{
  "first_name": "string",
  "last_name": "string",
  "phone": "string",
  "organization": "string",
  "profile_picture": "file"
}
```

**Expected Response (200 OK):** Updated user object

#### List All Users (Admin Only)
**Endpoint:** `GET /api/users/list/`

**Required:** Admin authentication

**Expected Response (200 OK):**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/users/list/?page=2",
  "previous": null,
  "results": [
    {
      "username": "user1",
      "email": "user1@example.com",
      "role": "STUDENT",
      ...
    }
  ]
}
```

#### Approve Vendor Account (Admin Only)
**Endpoint:** `POST /api/users/approve-vendor/<user_id>/`

**Required:** Admin authentication

**Input:** No body required

**Expected Response (200 OK):**
```json
{
  "status": "Vendor johndoe approved."
}
```

---

### 2. Catalog (Equipment Listing)

#### Get All Equipment (Searchable & Filterable)
**Endpoint:** `GET /api/catalog/equipment/`

**Optional Query Parameters:**
- `name`: Filter by equipment name
- `category`: Filter by category ID
- `brand`: Filter by brand
- `min_price`: Minimum rental price per day
- `max_price`: Maximum rental price per day
- `search`: General search across name, brand, model

**Example:** `/api/catalog/equipment/?search=microscope&max_price=500`

**Expected Response (200 OK):**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/catalog/equipment/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Compound Microscope",
      "brand": "Zeiss",
      "model_number": "ZM-2000",
      "description": "Professional compound microscope for laboratory use",
      "category_name": "Microscopes",
      "vendor_name": "LabEquipment Inc",
      "rental_price_per_day": "150.00",
      "purchase_price": "5000.00",
      "availability_count": 3,
      "image": "https://api.example.com/equipment_photos/microscope_1.jpg"
    }
  ]
}
```

#### Get Equipment Details
**Endpoint:** `GET /api/catalog/equipment/<equipment_id>/`

**Expected Response (200 OK):** Single equipment object (see above)

#### Create Equipment with Units (Vendor Only)
**Endpoint:** `POST /api/catalog/manage/`

**Required:** Vendor authentication

**Input:**
```json
{
  "name": "Compound Microscope",
  "brand": "Zeiss",
  "model_number": "ZM-2000",
  "description": "Professional compound microscope",
  "category": 1,
  "rental_price_per_day": "150.00",
  "purchase_price": "5000.00",
  "image": "file",
  "serial_numbers": ["SN-001", "SN-002", "SN-003"]
}
```

**Expected Response (201 Created):**
```json
{
  "id": 1,
  "name": "Compound Microscope",
  "brand": "Zeiss",
  "model_number": "ZM-2000",
  "description": "Professional compound microscope",
  "category_name": "Microscopes",
  "vendor_name": "current_user",
  "rental_price_per_day": "150.00",
  "purchase_price": "5000.00",
  "availability_count": 3,
  "image": "https://api.example.com/equipment_photos/microscope_1.jpg"
}
```

#### Update Equipment (Vendor Only)
**Endpoint:** `PUT/PATCH /api/catalog/manage/<equipment_id>/`

**Required:** Vendor authentication (must be equipment owner)

**Input:** Any fields to update (same as creation)

#### Delete Equipment (Vendor Only)
**Endpoint:** `DELETE /api/catalog/manage/<equipment_id>/`

**Required:** Vendor authentication (must be equipment owner)

---

### 3. Inventory Management

#### Get All Equipment Units
**Endpoint:** `GET /api/inventory/`

**Query Parameters:**
- `status`: Filter by status (AVAILABLE, RENTED, SOLD, MAINTENANCE, CALIBRATION, DAMAGED)

**For Students:** Only returns AVAILABLE units
**For Vendors:** Returns all units they own

**Expected Response (200 OK):**
```json
{
  "count": 50,
  "results": [
    {
      "id": 1,
      "equipment": {
        "id": 5,
        "name": "Compound Microscope",
        "brand": "Zeiss",
        "model_number": "ZM-2000",
        "image": "https://..."
      },
      "serial_number": "SN-001",
      "internal_id": "LAB-001",
      "status": "AVAILABLE",
      "last_calibration_date": "2026-03-15",
      "next_maintenance_due": "2026-06-15"
    }
  ]
}
```

#### Get Equipment Unit Details
**Endpoint:** `GET /api/inventory/<unit_id>/`

**Expected Response (200 OK):** Single unit object (see above)

#### Check In Equipment Unit (Vendor Only)
**Endpoint:** `POST /api/inventory/<unit_id>/check_in/`

**Required:** Vendor authentication

**Input:**
```json
{
  "has_damage": true/false,
  "description": "string (if damaged)"
}
```

**Expected Response (200 OK):**
```json
{
  "status": "Check-in successful. Unit is AVAILABLE. Incident filed against student_name."
}
```

---

### 4. Bookings & Reservations

#### Create Booking (Rental or Purchase)
**Endpoint:** `POST /api/bookings/`

**Required:** Authentication (JWT Token)

**Input:**
```json
{
  "unit": 1,
  "booking_type": "RENTAL | PURCHASE",
  "start_date": "2026-06-01",
  "end_date": "2026-06-05",
  "pick_up_location": "Main Lab Building Room 101",
  "drop_off_location": "Main Lab Building Room 101"
}
```

**Expected Response (201 Created):**
```json
{
  "checkout_url": "https://checkout.paystack.com/...",
  "reference": "TXN-12345",
  "booking data": {
    "id": 1,
    "unit": 1,
    "booking_type": "RENTAL",
    "status": "PENDING",
    "start_date": "2026-06-01",
    "end_date": "2026-06-05",
    "pick_up_location": "Main Lab Building Room 101",
    "drop_off_location": "Main Lab Building Room 101",
    "pick_up_date": null,
    "drop_off_date": null
  }
}
```

#### Get User's Bookings
**Endpoint:** `GET /api/bookings/`

**Required:** Authentication (JWT Token)

**For Students:** Returns their own bookings
**For Vendors:** Returns bookings of their equipment

**Expected Response (200 OK):**
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "unit": 1,
      "booking_type": "RENTAL",
      "status": "CONFIRMED",
      "start_date": "2026-06-01",
      "end_date": "2026-06-05",
      "pick_up_location": "Main Lab Building",
      "drop_off_location": "Main Lab Building",
      "pick_up_date": "2026-06-01T10:30:00Z",
      "drop_off_date": null
    }
  ]
}
```

#### Get Booking Details
**Endpoint:** `GET /api/bookings/<booking_id>/`

**Required:** Authentication (JWT Token)

**Expected Response (200 OK):** Single booking object

#### Update Booking (Before Payment)
**Endpoint:** `PUT/PATCH /api/bookings/<booking_id>/`

**Required:** Authentication, must be booking owner or vendor

**Input:** Any fields to update

#### Cancel Booking
**Endpoint:** `DELETE /api/bookings/<booking_id>/`

**Required:** Authentication, must be booking owner

---

### 5. Feedback & Incident Reports

#### Submit Feedback/Rating
**Endpoint:** `POST /api/feedback/reviews/`

**Required:** Authentication (JWT Token)

**Input:**
```json
{
  "equipment_unit": 1,
  "rating": 4,
  "comment": "Great microscope, very accurate"
}
```

**Note:** Rating must be between 1-5. A user can only review each physical unit once.

**Expected Response (201 Created):**
```json
{
  "id": 1,
  "user": 1,
  "equipment_unit": 1,
  "rating": 4,
  "comment": "Great microscope, very accurate",
  "created_at": "2026-05-31T10:30:00Z"
}
```

#### Get Equipment Feedback
**Endpoint:** `GET /api/feedback/reviews/`

**Query Parameters:**
- `equipment_unit`: Filter by unit ID

**Expected Response (200 OK):**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "user": 1,
      "equipment_unit": 1,
      "rating": 4,
      "comment": "Great microscope",
      "created_at": "2026-05-31T10:30:00Z"
    }
  ]
}
```

#### Report Incident/Damage
**Endpoint:** `POST /api/feedback/incidents/`

**Required:** Authentication (Vendor/Staff reporting)

**Input:**
```json
{
  "equipment_unit": 1,
  "target_user": 5,
  "incident_type": "DAMAGE | MALFUNCTION | VANDALISM | LATE_RETURN | OTHER",
  "description": "Equipment screen was cracked during use"
}
```

**Note:** Reporter is automatically set to current user. Cannot report yourself.

**Expected Response (201 Created):**
```json
{
  "id": 1,
  "equipment_unit": 1,
  "reporter": "staff_member",
  "target_user": "student_name",
  "incident_type": "DAMAGE",
  "description": "Equipment screen was cracked",
  "resolved": false,
  "reported_at": "2026-05-31T10:30:00Z",
  "reporter_name": "staff_member",
  "target_user_name": "student_name",
  "unit_serial": "SN-001"
}
```

#### Get Incident Reports
**Endpoint:** `GET /api/feedback/incidents/`

**Required:** Authentication

**Expected Response (200 OK):** List of incident report objects

#### Get Admin Dashboard Analytics
**Endpoint:** `GET /api/feedback/dashboard/`

**Required:** Admin authentication

**Expected Response (200 OK):**
```json
{
  "fleet_health": {
    "total_units": 150,
    "damaged_units": 5,
    "health_percentage": 96.67
  },
  "finance": {
    "total_revenue_kes": 125000.00
  },
  "incidents": {
    "total_reports": 12,
    "vandalism_cases": 2,
    "high_risk_students": [
      {
        "target_user__username": "risky_student",
        "report_count": 3
      }
    ]
  },
  "pending_repairs": 3
}
```

---

### 6. Payments

#### Payment Callback (Paystack)
**Endpoint:** `GET /api/payments/callback/?reference=<transaction_reference>`

**Purpose:** Redirect endpoint after customer completes payment on Paystack

**Expected Response (200 OK):**
```json
{
  "message": "Payment received. Awaiting confirmation.",
  "reference": "TXN-12345"
}
```

#### Payment Webhook (Paystack → Backend)
**Endpoint:** `POST /api/payments/webhook/`

**Note:** This is for Paystack to send payment confirmation. Frontend does NOT call this.

**Paystack will send:**
```json
{
  "event": "charge.success",
  "data": {
    "reference": "TXN-12345",
    ...other paystack data
  }
}
```

**Backend Response:** `{"status": "success"}`

---

### 7. Notifications

#### Get User Notifications
**Endpoint:** `GET /api/alerts/notifications/`

**Required:** Authentication (JWT Token)

**Query Parameters:**
- `is_read`: Filter by read status (true/false)

**Expected Response (200 OK):**
```json
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "user": 1,
      "notification_type": "MAINTENANCE",
      "message": "Equipment SN-001 requires maintenance",
      "created_at": "2026-05-31T10:30:00Z",
      "is_read": false
    }
  ]
}
```

#### Mark Notification as Read
**Endpoint:** `POST /api/alerts/notifications/<notification_id>/mark_read/`

**Required:** Authentication (JWT Token)

**Input:** No body required

**Expected Response (200 OK):**
```json
{
  "status": "notification marked as read"
}
```

#### Mark All Notifications as Read
**Endpoint:** `POST /api/alerts/notifications/mark_all_read/`

**Required:** Authentication (JWT Token)

**Input:** No body required

**Expected Response (200 OK):**
```json
{
  "status": "all notifications marked as read"
}
```

---

### 8. Transactions

#### Get User Transactions
**Endpoint:** `GET /api/transactions/transaction-history/`

**Required:** Authentication (JWT Token)

**For Students:** Returns their own transactions
**For Vendors:** Returns transactions for their equipment
**For Admins:** Returns all transactions

**Expected Response (200 OK):**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "booking_id": 10,
      "equipment_name": "Compound Microscope",
      "amount": "750.00",
      "status": "COMPLETED",
      "provider_reference": "PAY-001",
      "created_at": "2026-05-31T10:30:00Z"
    }
  ]
}
```

#### Get Transaction Details
**Endpoint:** `GET /api/transactions/transaction-history/<transaction_id>/`

**Required:** Authentication (JWT Token)

**Expected Response (200 OK):** Single transaction object

---

## Error Handling

### Common HTTP Status Codes

| Code | Meaning | Example Response |
|------|---------|------------------|
| 200 | Success | Standard response with data |
| 201 | Created | Resource successfully created |
| 400 | Bad Request | `{"detail": "Invalid input"}` |
| 401 | Unauthorized | `{"detail": "Authentication credentials not provided"}` |
| 403 | Forbidden | `{"detail": "Permission denied"}` |
| 404 | Not Found | `{"detail": "Not found"}` |
| 422 | Validation Error | `{"field_name": ["Error message"]}` |
| 500 | Server Error | `{"error": "Server error"}` |

---

## Frontend Integration Checklist

### Authentication Flow
- [ ] Implement registration form with username, email, password, role selection
- [ ] Implement login form and store JWT tokens (access + refresh)
- [ ] Auto-refresh token when expired
- [ ] Clear tokens on logout
- [ ] Add Authorization header to all authenticated requests

### Student/Researcher Flow
- [ ] Create equipment search/filter page
- [ ] Display equipment details with availability count
- [ ] Create booking form with date selection
- [ ] Redirect to Paystack checkout URL after booking
- [ ] Show booking status (PENDING → CONFIRMED → ACTIVE → COMPLETED)
- [ ] Allow feedback submission after booking completed
- [ ] Show notification center with maintenance/booking reminders
- [ ] Display transaction history

### Vendor Flow
- [ ] Create equipment listing form with serial numbers
- [ ] Display vendor's equipment with stock status
- [ ] Handle check-in process with damage reporting
- [ ] File incident reports against students if needed
- [ ] View bookings of their equipment
- [ ] See transaction history for their equipment

### Admin Flow
- [ ] Dashboard with fleet health metrics
- [ ] Revenue tracking
- [ ] Incident analysis (vandalism vs accidents)
- [ ] High-risk student identification
- [ ] Vendor approval management
- [ ] View all users and bookings

---

## Environment Variables

Required `.env` file variables:
```
DATABASE_URL=postgresql://user:password@localhost:5432/smartlab_db
SECRET_KEY=your-django-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
PAYSTACK_PUBLIC_KEY=pk_...
PAYSTACK_SECRET_KEY=sk_...
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

---

## Notes for Frontend Developers

1. **Date Format:** All dates use ISO 8601 format (YYYY-MM-DD and YYYY-MM-DDTHH:MM:SSZ)
2. **Pagination:** List endpoints use default pagination. Check `next` and `previous` fields
3. **Filtering:** Most list endpoints support filtering via query parameters
4. **Images:** Profile pictures and equipment images are returned as full URLs
5. **Decimal Numbers:** Prices and amounts are returned as strings (decimal format)
6. **JWT Token Expiry:** Access tokens expire after a set period (check with backend)
7. **CORS:** Ensure frontend domain is whitelisted in backend settings
8. **File Uploads:** Use multipart/form-data for endpoints accepting files
9. **Testing:** Use Insomnia or Postman to test endpoints before frontend integration
10. **Error Messages:** Always display user-friendly error messages from response data