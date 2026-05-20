from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Booking
        fields = ['id', 'user', 'unit', 'booking_type', 'status', 'start_date', 'end_date', 
                  'pick_up_location', 'drop_off_location', 'pick_up_date', 'drop_off_date']
        read_only_fields = ['status']

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be after start date.")
        
        return data
