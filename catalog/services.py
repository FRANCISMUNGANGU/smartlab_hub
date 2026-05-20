from django.db import transaction
from .models import Equipment
from inventory.models import EquipmentUnit


class CatalogService:
    @staticmethod
    @transaction.atomic
    def create_equipment_with_units(vendor, data, serial_numbers=None):
        """
        Atomic service to ensure equipment and its units are created together.
        """
        if not serial_numbers:
            serial_numbers = []

        # 1. Create the base Equipment record
        equipment = Equipment.objects.create(
            vendor=vendor,
            **data
        )

        # 2. Create the physical units (MUST be inside the 'with' block)
        for sn in serial_numbers:
            EquipmentUnit.objects.create(
                equipment=equipment,
                serial_number=sn,
                status=EquipmentUnit.Status.AVAILABLE
            )

        return equipment