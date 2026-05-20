from django.dispatch import Signal

# This signal will carry the transaction object as its 'message'
payment_confirmed = Signal()