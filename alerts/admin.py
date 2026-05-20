from django.contrib import admin
from .models import NotificationLog

# Register your models here.
@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('equipment_unit', 'user', 'notification_type', 'sent_at', 'message')
    list_filter = ('notification_type', 'sent_at')
    search_fields = ('equipment_unit__serial_number', 'user__username')