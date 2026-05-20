from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from bookings.models import Booking
from inventory.models import EquipmentUnit
from .serializers import NotificationLog
from .services import AlertService

@shared_task
def check_return_reminders():
    now = timezone.now()
    # 1. Check for 24-hour reminders
    target_24h = now + timedelta(hours=24)
    upcoming_24h = Booking.objects.filter(
        end_date__date=target_24h.date(), 
        status="ACTIVE"
    )
    
    for booking in upcoming_24h:
        send_notification(booking.user, "Your rental is due in 24 hours!", alert_type="REMINDER")

    # 2. Check for 1-hour reminders
    target_1h = now + timedelta(hours=1)
    upcoming_1h = Booking.objects.filter(
        end_date__date=target_1h.date(), 
        status="ACTIVE"
    )
    for booking in upcoming_1h:
        send_notification(booking.user, "Your rental is due in 1 hour!", alert_type="REMINDER")

    # 3. Check for overdue alerts
    overdue_bookings = Booking.objects.filter(
        end_date__date__lt=now.date(),
        status="ACTIVE"
    )
    for booking in overdue_bookings:
        send_notification(booking.user, "Your rental is overdue! Please return it as soon as possible.", alert_type="OVERDUE")
        booking.status = "OVERDUE"
        booking.save()

@shared_task
def check_maintenance_alerts():
    # Logic for 1 month, 1 week, 1 day for Vendors
    now = timezone.now()
    target_1m = now + timedelta(days=30)
    target_1w = now + timedelta(days=7)
    target_1d = now + timedelta(days=1)

    for unit in EquipmentUnit.objects.filter(status=EquipmentUnit.Status.AVAILABLE):
        if unit.next_maintenance_due:
            if unit.next_maintenance_due == target_1m.date():
                send_notification_to_vendor(unit, "Maintenance due in 1 month", alert_type="MAINTENANCE")
            elif unit.next_maintenance_due == target_1w.date():
                send_notification_to_vendor(unit, "Maintenance due in 1 week", alert_type="MAINTENANCE")
            elif unit.next_maintenance_due == target_1d.date():
                send_notification_to_vendor(unit, "Maintenance due in 1 day", alert_type="MAINTENANCE")

@shared_task
def check_calibration_alerts():
    now = timezone.now()
    target_1m = now + timedelta(days=30)
    target_1w = now + timedelta(days=7)
    target_1d = now + timedelta(days=1)

    for unit in EquipmentUnit.objects.filter(status=EquipmentUnit.Status.AVAILABLE):
        if unit.last_calibration_date:
            next_calibration_due = unit.last_calibration_date + timedelta(days=180)  # Assuming calibration is due every 6 months
            if next_calibration_due == target_1m.date():
                send_notification_to_vendor(unit, "Calibration due in 1 month", alert_type="CALIBRATION")
            elif next_calibration_due == target_1w.date():
                send_notification_to_vendor(unit, "Calibration due in 1 week", alert_type="CALIBRATION")
            elif next_calibration_due == target_1d.date():
                send_notification_to_vendor(unit, "Calibration due in 1 day", alert_type="CALIBRATION")





def send_notification(user, message, alert_type="INFO"):
    """
    Creates a persistent notification in the database for a specific user.
    """
    AlertService.create_notification(user=user, message=message, alert_type=alert_type)

def send_notification_to_vendor(unit, message, alert_type="MAINTENANCE"):
    """
    Finds the vendor associated with a piece of equipment and alerts them.
    """
    vendor = unit.equipment.vendor
    send_notification(user=vendor, message=message, alert_type=alert_type)