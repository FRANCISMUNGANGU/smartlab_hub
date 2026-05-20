from django.db import models
from django.conf import settings

# Create your models here.
class Booking(models.Model):
    class BookingType(models.TextChoices):
        RENTAL = "RENTAL", "Rental"
        PURCHASE = "PURCHASE", "Purchase"
    
    class BookingStatus(models.TextChoices):
        PENDING = "PENDING", "Pending payment"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"
        ACTIVE = "ACTIVE", "Active/In use"
        COMPLETED = "COMPLETED", "Completed/Returned"
        OVERDUE = "OVERDUE", "Overdue"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_bookings')
    unit = models.ForeignKey('inventory.EquipmentUnit', on_delete=models.CASCADE, related_name='bookings')
    booking_type = models.CharField(max_length=20, choices=BookingType.choices)
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    pick_up_location = models.CharField(max_length=255, blank=True, null=True)
    drop_off_location = models.CharField(max_length=255, blank=True, null=True)

    pick_up_date = models.DateTimeField(blank=True, null=True)
    drop_off_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.booking_type} - {self.unit.equipment.name} for {self.user.username} from {self.start_date} to {self.end_date}"