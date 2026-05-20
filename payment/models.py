from django.db import models

# Create your models here.
class Payment(models.Model):
    transaction = models.OneToOneField('transactions.Transaction', on_delete=models.CASCADE, related_name='payment')
    payload = models.JSONField()  # Stores the entire Paystack response
    provider_reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.provider_reference} - {self.status}"