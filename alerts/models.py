from django.db import models
from django.conf import settings

# Create your models here.

class NotificationLog(models.Model):
    class NotificationType(models.TextChoices):
        MAINTENANCE = "MAINTENANCE", "Maintenance Reminder"
        CALIBRATION = "CALIBRATION", "Calibration Reminder"
        BOOKING_REMINDER = "BOOKING_REMINDER", "Booking Reminder"
        OVERDUE_ALERT = "OVERDUE_ALERT", "Overdue Alert"

    equipment_unit = models.ForeignKey(
        'inventory.EquipmentUnit', 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.notification_type} for {self.equipment_unit.serial_number} at {self.sent_at}"