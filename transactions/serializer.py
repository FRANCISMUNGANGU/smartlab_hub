from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    # We bring in some booking info so the student knows what they are paying for
    booking_id = serializers.ReadOnlyField(source='booking.id')
    equipment_name = serializers.ReadOnlyField(source='booking.unit.equipment.name')
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'booking_id', 'equipment_name', 'amount', 
            'status', 'transaction_reference', 'created_at'
        ]
        # We make status and provider_ref read-only so the student 
        # can't manually tell the API "I have paid"
        read_only_fields = ['status', 'amount', 'transaction_reference', 'created_at']