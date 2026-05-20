from django.db import models
from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Equipment(models.Model):
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='equipment_listings',
        limit_choices_to={'role': 'VENDOR'}
    )

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    description = models.TextField()
    
    # Base Pricing
    rental_price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Meta tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='equipment_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.name} ({self.model_number})"
    