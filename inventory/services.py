from datetime import date, timezone
from django.db import transaction
from django.db.models import Q
from .models import EquipmentUnit, MaintenanceLog
from feedback.services import FeedbackService
import datetime, time

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
        start_datetime = datetime.combine(start_date, time.min)
        end_datetime = datetime.combine(end_date, time.max)

        aware_start_date = timezone.make_aware(start_datetime, timezone.get_current_timezone())
        aware_end_date = timezone.make_aware(end_datetime, timezone.get_current_timezone())


        for unit in candidates:
            # Check for overlapping bookings
            has_booking = unit.bookings.filter(
                Q(start_date__lte=aware_end_date) & Q(end_date__gte=aware_start_date)
            ).exists()

            # Check for planned maintenance/calibration
            has_maintenance = unit.maintenance_history.filter(
                Q(start_date__lte=aware_end_date) & Q(end_date__gte=aware_start_date) & Q(is_completed=False)
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
    
    def update_unit_status(self, unit_id, new_status):
        """
        Admin function to manually update the status of an equipment unit.
        """
        unit = EquipmentUnit.objects.get(id=unit_id)
        unit.status = new_status
        unit.save()
        return unit