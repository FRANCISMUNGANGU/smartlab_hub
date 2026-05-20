from rest_framework import serializers
from .models import Feedback, IncidentReport

class IncidentReportSerializer(serializers.ModelSerializer):
    # Helpful read-only fields for the frontend
    reporter_name = serializers.ReadOnlyField(source='reporter.username')
    target_user_name = serializers.ReadOnlyField(source='target_user.username')
    unit_serial = serializers.ReadOnlyField(source='equipment_unit.serial_number')

    class Meta:
        model = IncidentReport
        fields = [
            'id', 'equipment_unit', 'reporter', 'target_user', 
            'incident_type', 'description', 'resolved', 
            'reported_at', 'reporter_name', 'target_user_name', 'unit_serial'
        ]
        # We make the 'reporter' and 'reported_at' read-only 
        # because the system should handle these automatically.
        read_only_fields = ['id', 'reporter', 'reported_at']

    def validate(self, data):
        # Prevent reporting yourself
        if self.context['request'].user == data.get('target_user'):
            raise serializers.ValidationError("You cannot file an incident report against yourself.")
        return data
    

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'equipment_unit', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value