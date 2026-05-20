from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from users.factories import UserFactory, EquipmentFactory, EquipmentUnitFactory
from inventory.models import EquipmentUnit

class InventoryModelTest(TestCase):
    def test_unit_creation_with_factories(self):
        # This one line creates: A Vendor User, an Equipment Listing, AND a Unit!
        unit = EquipmentUnitFactory()
        
        self.assertEqual(unit.status, EquipmentUnit.Status.AVAILABLE)
        self.assertTrue(unit.serial_number) # Faker generated a real-looking UUID
        
    def test_maintenance_status_change(self):
        # Create a unit that is specifically marked as maintenance
        unit = EquipmentUnitFactory(status=EquipmentUnit.Status.MAINTENANCE)
        self.assertEqual(unit.status, "MAINTENANCE")