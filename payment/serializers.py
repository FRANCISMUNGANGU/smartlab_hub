from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'transaction', 'payload', 'provider_reference', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_provider_reference(self, value):
        if Payment.objects.filter(provider_reference=value).exists():
            raise serializers.ValidationError("This provider reference already exists.")
        return value