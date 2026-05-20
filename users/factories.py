import factory
from factory.django import DjangoModelFactory
from users.models import User
from catalog.models import Category, Equipment
from inventory.models import EquipmentUnit

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    role = User.Roles.STUDENT  # Default role, can be overridden when creating instances

class EquipmentFactory(DjangoModelFactory):
    class Meta:
        model = Equipment

    vendor = factory.SubFactory(UserFactory, role='VENDOR')
    name = factory.Faker('word')
    brand = factory.Faker('company')
    model_number = factory.Faker('bothify', text='MOD-####-??')
    rental_price_per_day = 500.00
    purchase_price = 50000.00

class EquipmentUnitFactory(DjangoModelFactory):
    class Meta:
        model = EquipmentUnit

    equipment = factory.SubFactory(EquipmentFactory)
    serial_number = factory.Faker('uuid4')
    status = EquipmentUnit.Status.AVAILABLE