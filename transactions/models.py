from django.db import models

class Transaction(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    booking = models.OneToOneField(
        'bookings.Booking', 
        on_delete=models.CASCADE, 
        related_name='transaction'
    )
    
    # NEW: Store the actual KES amount charged
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    transaction_reference = models.CharField(
        max_length=100, 
        unique=True, 
        null=True, # Allow null initially while PENDING
        blank=True
    )
    
    status = models.CharField(
        max_length=20, 
        choices=PaymentStatus.choices, 
        default=PaymentStatus.PENDING
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"TXN-{self.id} for {self.booking.user.username} ({self.status})"