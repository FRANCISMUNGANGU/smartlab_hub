from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    # Add any additional fields you want for your user model here
    class Roles(models.TextChoices):
        # not to be access by user
        ADMIN = 'ADMIN', 'Admin'
        # expose to DRF API
        RESEARCHER = 'RESEARCHER', 'Researcher'
        STUDENT = 'STUDENT', 'Student'
        VENDOR = 'VENDOR', 'Vendor'
    
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.STUDENT)
    phone = models.CharField(max_length=20, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    # Vendor-specific fields
    pickup_location = models.CharField(max_length=255, blank=True, null=True, help_text="Default pickup location for equipment rentals")
    dropoff_location = models.CharField(max_length=255, blank=True, null=True, help_text="Default drop-off location for equipment returns")

    def save(self, *args, **kwargs):
        # Ensure that the role is valid before saving
        if self.role not in self.Roles.values:
            raise ValueError(f"Invalid role: {self.role}")
        super().save(*args, **kwargs)