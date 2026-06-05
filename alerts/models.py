from django.db import models
from django.conf import settings

# Create your models here.

class NotificationLog(models.Model):
    class NotificationType(models.TextChoices):
        INFO = "INFO", "Info"
        SYSTEM = "SYSTEM", "System"
        ROLE_CHANGE = "ROLE_CHANGE", "Role Change"
        PAYMENT = "PAYMENT", "Payment"
        MAINTENANCE = "MAINTENANCE", "Maintenance Reminder"
        CALIBRATION = "CALIBRATION", "Calibration Reminder"
        BOOKING_REMINDER = "BOOKING_REMINDER", "Booking Reminder"
        OVERDUE_ALERT = "OVERDUE_ALERT", "Overdue Alert"

    equipment_unit = models.ForeignKey(
        'inventory.EquipmentUnit',
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    
    notification_type = models.CharField(max_length=30, choices=NotificationType.choices, default=NotificationType.INFO)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        unit_name = self.equipment_unit.serial_number if self.equipment_unit else 'General'
        return f"{self.notification_type} for {unit_name} at {self.sent_at}"