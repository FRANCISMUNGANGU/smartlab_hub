from rest_framework import serializers
from .models import Booking
from inventory.serializers import EquipmentUnitSerializer
from inventory.models import EquipmentUnit
from transactions.serializer import TransactionSerializer


class BookingSerializer(serializers.ModelSerializer):

    start_date = serializers.DateTimeField(allow_null=True, required=False)
    end_date = serializers.DateTimeField(allow_null=True, required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    unit = serializers.PrimaryKeyRelatedField(queryset=EquipmentUnit.objects.all())
    transaction = TransactionSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'unit', 'transaction', 'booking_type', 'status', 'start_date', 'end_date', 
                  'pick_up_location', 'drop_off_location', 'pick_up_date', 'drop_off_date', 'created_at']
        read_only_fields = ['status', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['unit'] = EquipmentUnitSerializer(instance.unit).data
        return data

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # Ensure BOTH values are present and are not None
        if start_date is not None and end_date is not None:
            # Check if they are full datetime objects before calling .date()
            start_date_pure = start_date.date() if hasattr(start_date, 'date') else start_date
            end_date_pure = end_date.date() if hasattr(end_date, 'date') else end_date

            if start_date_pure > end_date_pure:
                raise serializers.ValidationError({
                    "end_date": "End date must be after start date."
                })
        return data
