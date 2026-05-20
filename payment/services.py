from .serializers import PaymentSerializer
from .models import Payment
import hmac
import hashlib
from django.conf import settings
from django.db import transaction as db_transaction
from django.apps import apps
import requests

class PaymentService:

    @staticmethod
    def initialize_payment(transaction):
        """
        Calls Paystack to get a checkout URL.
        """
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "email": transaction.booking.user.email,
            "amount": int(transaction.amount * 100), # Paystack uses Cents/Kobo
            "reference": transaction.transaction_reference,       # YOUR generated ID
            "callback_url": "https://fbd3-102-205-238-255.ngrok-free.app/api/payments/callback/",
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json() # This contains the 'authorization_url'

    @staticmethod
    def create_payment(transaction_obj, payload):
        
        data = payload.get('data', {})
        return Payment.objects.create(
            transaction=transaction_obj,
            payload=payload,
            provider_reference=data.get('reference'),
            status=data.get('status')
        )
    
    @staticmethod
    def verify_webhook(payload, signature):
        """
        The 'Scalable' way to verify signatures.
        """
        secret = settings.PAYSTACK_SECRET_KEY.encode('utf-8')
        computed_hmac = hmac.new(
            secret, 
            payload, 
            hashlib.sha512
        ).hexdigest()
        
        return hmac.compare_digest(computed_hmac, signature)
    
    @staticmethod
    def process_successful_payment(transaction_id):
        """
        The Bridge: Updates the Transaction and the Booking.
        """
        # Using apps.get_model prevents 'Circular Import' errors 
        # that would definitely cook a Waterfall dev.
        Transaction = apps.get_model('transactions', 'Transaction')        
        with db_transaction.atomic():
            # select_for_update() locks the row so two webhooks don't clash
            txn = Transaction.objects.select_for_update().get(id=transaction_id)
            
            if txn.status == Transaction.PaymentStatus.COMPLETED:
                return  # Already processed

            txn.status = Transaction.PaymentStatus.COMPLETED
            txn.save()

            # Reach through the OneToOne to the Booking
            booking = txn.booking
            booking.status = 'CONFIRMED'
            booking.save()