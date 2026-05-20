from datetime import date
from django.db import transaction
from django.db.models import Q
from .models import EquipmentUnit, MaintenanceLog
from feedback.services import FeedbackService

class InventoryService:
    
    @staticmethod
    def get_available_unit(equipment_id, start_date, end_date):
        """
        Finds ONE available unit for a specific equipment type and date range.
        """
        # 1. Get all potential candidates (exclude hard statuses like SOLD)
        candidates = EquipmentUnit.objects.filter(
            equipment_id=equipment_id,
            status=EquipmentUnit.Status.AVAILABLE
        )

        for unit in candidates:
            # Check for overlapping bookings
            has_booking = unit.bookings.filter(
                Q(start_date__lte=end_date) & Q(end_date__gte=start_date)
            ).exists()

            # Check for planned maintenance/calibration
            has_maintenance = unit.maintenance_history.filter(
                Q(start_date__lte=end_date) & Q(end_date__gte=start_date) & Q(is_completed=False)
            ).exists()

            if not has_booking and not has_maintenance:
                return unit # Found a free one!
        
        return None # No units free for these dates

    @staticmethod
    @transaction.atomic
    def process_check_in(unit, vendor, has_damage, description=None):
        """
        Handles the return, updates statuses, and files reports.
        """
        student = unit.last_student
        if not student:
            raise ValueError("No record of a student using this unit.")

        # 1. Update Unit Status
        unit.status = 'DAMAGED' if has_damage else 'AVAILABLE'
        unit.save()

        # 2. Complete the Booking
        active_booking = unit.current_booking
        if active_booking:
            active_booking.status = 'COMPLETED'
            active_booking.save()

        # 3. File Incident and create Maintenance log if needed
        if has_damage:
            # File the formal incident for the Admin Analysis
            FeedbackService.record_incident(
                reporter=vendor,
                unit=unit,
                target_user=student,
                incident_type='DAMAGE',
                description=description or 'Damage reported during check-in.'
            )
            
            # Create the log for the technician
            MaintenanceLog.objects.create(
                equipment_unit=unit,
                start_date=date.today(),
                technician_notes=f"Damage reported on return by {vendor.username}: {description}",
                is_completed=False
            )
        
        return student