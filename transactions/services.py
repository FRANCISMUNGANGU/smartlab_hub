from datetime import timedelta

from django.db import transaction
from alerts.models import NotificationLog
from .models import Transaction

class TransactionService:
    @staticmethod
    def create_transaction_for_booking(booking, total_price):
        """
        Calculate the total price for a booking based on its type and duration.
        For rentals, the price is calculated as rental_price_per_day * number of days.
        For purchases, the price is simply the purchase_price of the equipment.

        Create a Transaction record with the calculated price and link it to the booking.
        """

        # Create the transaction record
        transaction = Transaction.objects.create(
            booking=booking,
            transaction_reference=f"TXN-{booking.id}-{booking.created_at.timestamp()}",
            status=Transaction.PaymentStatus.PENDING,
            amount=total_price
        )

        return transaction
    
    @staticmethod
    @transaction.atomic
    def fulfill_transaction(transaction_id):
        tx = Transaction.objects.select_for_update().get(id=transaction_id)
        
        if tx.status == Transaction.PaymentStatus.COMPLETED:
            return tx # Already processed

        # 1. Update Transaction
        tx.status = Transaction.PaymentStatus.COMPLETED
        # tx.provider_reference = provider_reference
        tx.save()

        # 2. Confirm the Booking
        booking = tx.booking
        booking.status = 'CONFIRMED'
        booking.save()

        # 3. Notify Vendor
        NotificationLog.objects.create(
            user=booking.unit.equipment.vendor,
            notification_type="PAYMENT",
            message=f"Payment confirmed for {booking.unit.equipment.name}. Prepare for pickup."
        )

        # 4. Notify Student about next steps (pickup instructions, etc.)
        NotificationLog.objects.create(
            user=booking.user,
            notification_type="INFO",
            message=f"Your payment for {booking.unit.equipment.name} has been confirmed. Please check your booking details for pickup instructions."
        )

        return tx
