"""
URL configuration for SmartLab_Hub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from feedback.views import AdminDashboardAnalysisView
from payment.views import PaystackWebhookView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .frontend_views import (
    LandingView, LoginView, RegisterView, DashboardView,
    EquipmentView, BookingsView, FeedbackView, ProfileView,
    VendorDashboardView, VendorEquipmentView, VendorInventoryView,
    VendorBookingsView, AdminDashboardView,
)


urlpatterns = [
    # ── FRONTEND PAGES ──
    path("", LandingView.as_view(), name="landing"),
    path("login", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("equipment", EquipmentView.as_view(), name="equipment"),
    path("equipment/<int:pk>", EquipmentView.as_view(), name="equipment-detail"),
    path("bookings", BookingsView.as_view(), name="bookings"),
    path("feedback", FeedbackView.as_view(), name="feedback"),
    path("profile", ProfileView.as_view(), name="profile"),
    # Vendor pages
    path("vendor/dashboard", VendorDashboardView.as_view(), name="vendor-dashboard"),
    path("vendor/equipment", VendorEquipmentView.as_view(), name="vendor-equipment"),
    path("vendor/inventory", VendorInventoryView.as_view(), name="vendor-inventory"),
    path("vendor/bookings", VendorBookingsView.as_view(), name="vendor-bookings"),
    # Admin page
    path("admin-dashboard", AdminDashboardView.as_view(), name="admin-dashboard-frontend"),
    # ── API & ADMIN ──

    path('admin/', admin.site.urls),
    
    # 1. User Management & Auth
    path('api/users/', include('users.urls')),
    
    # 2. The Catalog (Generic Gear)
    path('api/catalog/', include('catalog.urls')),
    
    # 3. The Inventory (Physical Units & Check-in)
    path('api/inventory/', include('inventory.urls')),
    
    # 4. Bookings & Reservations
    path('api/bookings/', include('bookings.urls')),
    
    # 5. Feedback & Incident Reports
    path('api/feedback/', include('feedback.urls')),
    
    # 6. Alerts & Notifications
    path('api/alerts/', include('alerts.urls')),
    
    # 7. Transactions & Payment History
    path('api/transactions/', include('transactions.urls')),
    
    # 8. Payments
    path('api/payments/', include('payment.urls')),

    # 9. Specialized Analysis & Webhooks (The "Global" endpoints)
    path('api/analysis/dashboard/', AdminDashboardAnalysisView.as_view(), name='admin-analysis'),
    path('api/payments/callback/', PaystackWebhookView.as_view(), name='payment-callback'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Use this to get a new token when the old one expires
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)