from django.db import transaction
from django.utils import timezone
from datetime import datetime, time
from transactions.services import TransactionService
from .models import Booking
from inventory.models import EquipmentUnit
from catalog.models import Equipment
from transactions.models import Transaction


class BookingService:
    @staticmethod
    @transaction.atomic
    def create_lab_booking(user, equipment, start_date, end_date, booking_type,
                           pick_up_location=None, drop_off_location=None):
        
        # 1. AVAILABILITY CHECK
        unit = EquipmentUnit.objects.filter(equipment=equipment.equipment, status='AVAILABLE').first()
        vendor = Equipment.objects.get(id=equipment.equipment.id).vendor
        if not unit:
            raise ValueError("All units of this equipment are currently booked.")
        # 2. DATE VALIDATION (The Gatekeeper)
        if booking_type == 'RENTAL':
            if start_date.date() < timezone.now().date():
                raise ValueError("You cannot book lab equipment in the past.")
            if end_date.date() < start_date.date():
                raise ValueError("End date must be after start date.")


            start_datetime = datetime.combine(start_date.date(), time.min)
            end_datetime = datetime.combine(end_date.date(), time.max)

            aware_start_date = timezone.make_aware(start_datetime, timezone.get_current_timezone())
            aware_end_date = timezone.make_aware(end_datetime, timezone.get_current_timezone())
        

            # 3. PRICE CALCULATION (Keep logic here since it depends on dates)
            duration = (end_date - start_date).days
            days = max(1, duration + 1) # Ensure at least 1 day charge
            
            total_price = days * unit.equipment.rental_price_per_day
        
        
        total_price = unit.equipment.purchase_price

        # 4. CREATE THE BOOKING
        # Use custom location if provided, otherwise fall back to vendor's location
        # vendor_pickup = unit.equipment.user.profile.pickup_location
        vendor_pickup = vendor.pickup_location
        vendor_dropoff = vendor.dropoff_location


        booking = Booking.objects.create(
            user=user,
            unit=unit,
            start_date=aware_start_date if booking_type == 'RENTAL' else None,
            end_date=aware_end_date if booking_type == 'RENTAL' else None,
            booking_type=booking_type,
            status='PENDING',
            pick_up_location=pick_up_location or vendor_pickup,
            drop_off_location=drop_off_location or vendor_dropoff,
            pick_up_date=aware_start_date if booking_type == 'RENTAL' else None,
            drop_off_date=aware_end_date if booking_type == 'RENTAL' else None
        )

        # 5. HANDOFF TO ACCOUNTANT
        # We pass the pre-calculated price to ensure consistency
        transaction = TransactionService.create_transaction_for_booking(booking, total_price)

        return booking