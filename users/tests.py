from django.test import TestCase
from users.factories import UserFactory, EquipmentFactory, EquipmentUnitFactory
from inventory.models import EquipmentUnit

# Create your tests here.

class UserTestCase(TestCase):
    def test_user_creation_with_factories(self):
        user = UserFactory()
        self.assertTrue(user.username)
        self.assertTrue(user.email)
        self.assertEqual(user.role, 'STUDENT')  # Default role from factory
    
    def test_user_role_validation(self):
        with self.assertRaises(ValueError):
            UserFactory(role='INVALID_ROLE')
