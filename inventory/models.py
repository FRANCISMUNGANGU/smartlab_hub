from django.db import models

# Create your models here.
class EquipmentUnit(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        RENTED = "RENTED", "Rented"
        SOLD = "SOLD", "Sold"
        MAINTENANCE = "MAINTENANCE", "Maintenance"
        CALIBRATION = "CALIBRATION", "Calibration"
        DAMAGED = "DAMAGED", "Damaged"

    equipment = models.ForeignKey('catalog.Equipment', on_delete=models.CASCADE, related_name='units')
    serial_number = models.CharField(max_length=255, unique=True)
    internal_id = models.CharField(max_length=50, blank=True, help_text="Labs specific ID")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)

    # Track the last time it was serviced
    last_calibration_date = models.DateField(null=True, blank=True)
    next_maintenance_due = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.equipment.name} - {self.serial_number}"
    
    @property
    def current_booking(self):
        """Returns the active booking for this unit, if one exists."""
        # We look for 'ACTIVE' status. You could also check if 'now' 
        # falls between start_date and end_date.
        return self.bookings.filter(status='ACTIVE').first()

    @property
    def last_student(self):
        """Returns the User object of the student who most recently used this unit."""
        booking = self.current_booking or self.bookings.order_by('-end_date').first()
        return booking.user if booking else None
    
class MaintenanceLog(models.Model):
    equipment_unit = models.ForeignKey(
        EquipmentUnit,
        on_delete=models.CASCADE,
        related_name='maintenance_history'
        )
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    technician_notes = models.TextField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Maintenance for {self.equipment_unit.serial_number} from {self.start_date}"