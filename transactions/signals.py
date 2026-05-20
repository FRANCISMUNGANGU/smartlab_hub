from django.dispatch import receiver
from payment.signals import payment_confirmed
from .services import TransactionService


@receiver(payment_confirmed)
def handle_payment_confirmation(sender, transaction, **kwargs):
    """
    When the signal fires, we call the existing service logic.
    """
    # We call your fulfill_transaction method here
    TransactionService.fulfill_transaction(
        transaction_id=transaction.id, 
        # provider_reference=transaction.provider_reference # Passed from the signal/webhook
    )