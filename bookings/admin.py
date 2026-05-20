from django.contrib import admin
from .models import Booking
# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'unit', 'booking_type', 'status', 'start_date', 'end_date')
    list_filter = ('booking_type', 'status', 'start_date', 'end_date')
    search_fields = ('user__username', 'unit__serial_number')