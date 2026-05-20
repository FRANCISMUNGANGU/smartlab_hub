from django.db import models
from inventory.models import EquipmentUnit
from django.conf import settings

# Create your models here.
class IncidentReport(models.Model):
    class IncidentType(models.TextChoices):
        DAMAGE = "DAMAGE", "Damage"
        MALFUNCTION = "MALFUNCTION", "Malfunction"
        VANDALISM = "VANDALISM", "Vandalism"
        LATE_RETURN = "LATE_RETURN", "Late Return"
        OTHER = "OTHER", "Other"

    equipment_unit = models.ForeignKey(
        EquipmentUnit,
        on_delete=models.SET_NULL, 
        null=True,
        related_name='incidents'
    )
    
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports_made")
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="reports_received")
    
    incident_type = models.CharField(max_length=20, choices=IncidentType.choices)
    description = models.TextField()
    resolved = models.BooleanField(default=False)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Use getattr or check for None because equipment_unit is null=True
        unit_sn = self.equipment_unit.serial_number if self.equipment_unit else "Unknown Unit"
        return f"{self.incident_type} - {unit_sn} (Target: {self.target_user.username})"
    


class Feedback(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="feedbacks_given"
    )
    equipment_unit = models.ForeignKey(
        EquipmentUnit, 
        on_delete=models.CASCADE, 
        related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField() # We'll validate 1-5 in the serializer
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent a student from reviewing the same physical unit multiple times
        unique_together = ('user', 'equipment_unit')
        verbose_name_plural = "Feedback"

    def __str__(self):
        return f"Rating: {self.rating} for {self.equipment_unit.serial_number} by {self.user.username}"