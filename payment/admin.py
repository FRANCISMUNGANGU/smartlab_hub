from django.contrib import admin
from .models import Payment
# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'payload', 'provider_reference', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('transaction__booking__user__username', 'transaction__booking__unit__serial_number')