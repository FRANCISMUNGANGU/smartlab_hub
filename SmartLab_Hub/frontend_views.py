from django.shortcuts import render
from django.views.generic import TemplateView


class LandingView(TemplateView):
    template_name = 'index.html'


class LoginView(TemplateView):
    template_name = 'auth.html'


class RegisterView(TemplateView):
    template_name = 'auth.html'


class DashboardView(TemplateView):
    template_name = 'dashboard.html'


class EquipmentView(TemplateView):
    template_name = 'equipment.html'


class BookingsView(TemplateView):
    template_name = 'bookings.html'


class FeedbackView(TemplateView):
    template_name = 'feedback.html'


class ProfileView(TemplateView):
    template_name = 'profile.html'


# Vendor Views
class VendorDashboardView(TemplateView):
    template_name = 'vendor_dashboard.html'


class VendorEquipmentView(TemplateView):
    template_name = 'vendor_equipment.html'


class VendorInventoryView(TemplateView):
    template_name = 'vendor_inventory.html'


class VendorBookingsView(TemplateView):
    template_name = 'bookings.html'  # reuses bookings template with vendor context


# Admin View
class AdminDashboardView(TemplateView):
    template_name = 'admin_dashboard.html'