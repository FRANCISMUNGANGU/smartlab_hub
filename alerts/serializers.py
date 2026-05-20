from rest_framework import serializers
from .models import NotificationLog
from rest_framework import serializers
from .models import NotificationLog

class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(read_only=True)



class NotificationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationLog
        fields = ['id', 'user', 'alert_type', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'user', 'alert_type', 'message', 'created_at']
