from .models import NotificationLog
from django.db import transaction

class AlertService:
    @staticmethod
    @transaction.atomic
    def create_notification(user, data):
        """
        Service function to create a notification log entry.
        It uses transactions to ensure that the notification is created successfully, or not created if there's an error.
        """
        return NotificationLog.objects.create(
            user=user,
            **data
        )
