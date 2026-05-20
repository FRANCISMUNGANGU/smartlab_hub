from django.db import transaction
from .models import Feedback, IncidentReport
from bookings.models import Booking


class FeedbackService:
    @staticmethod
    @transaction.atomic
    def create_feedback(user, equipment_unit, rating, comment=None):
        """
        Service function to create feedback for a specific equipment unit.
        It uses transactions to ensure that the feedback is created successfully, or not created if there's an error.
        """
        has_rented = Booking.objects.filter(
            user=user,
            unit=equipment_unit,
            status__in=['ACTIVE', 'COMPLETED']
        ).exists()

        if not has_rented:
            raise ValueError("You can only leave feedback for equipment you have rented.")
        
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        
        if Feedback.objects.filter(user=user, equipment_unit=equipment_unit).exists():
            raise ValueError("You have already left feedback for this equipment unit.") 
        
        return Feedback.objects.create(
            user=user,
            equipment_unit=equipment_unit,
            rating=rating,
            comment=comment
        )
    
    @staticmethod
    @transaction.atomic

    def create_incident_report(reporter, target_user, equipment_unit, incident_type, description):
        """
        Service function to create an incident report for a specific equipment unit.
        It uses transactions to ensure that the report is created successfully, or not created if there's an error.
        """
        if reporter == target_user:
            raise ValueError("You cannot file an incident report against yourself.")
        
        return IncidentReport.objects.create(
            reporter=reporter,
            target_user=target_user,
            equipment_unit=equipment_unit,
            incident_type=incident_type,
            description=description
        )

