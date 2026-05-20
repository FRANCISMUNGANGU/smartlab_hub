from rest_framework import serializers
from .models import Equipment, Category
from inventory.models import EquipmentUnit

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class EquipmentUnitStatusSerializer(serializers.ModelSerializer):
    """Used to show availability status inside the Equipment detail view"""
    class Meta:
        model = EquipmentUnit
        fields = ['id', 'serial_number', 'status', 'next_maintenance_due']

class EquipmentSerializer(serializers.ModelSerializer):
    # Nested Serializers for better Readability
    category_name = serializers.ReadOnlyField(source='category.name')
    vendor_name = serializers.ReadOnlyField(source='vendor.username')
    
    # This allows the frontend to see if ANY units are available without extra API calls
    availability_count = serializers.SerializerMethodField()

    class Meta:
        model = Equipment
        fields = [
            'id', 'name', 'brand', 'model_number', 'description', 
            'category_name', 'vendor_name', 'rental_price_per_day', 
            'purchase_price', 'availability_count', 'image'
        ]

    def get_availability_count(self, obj):
        # Using the related_name='units' we defined in the Inventory model
        return obj.units.filter(status='AVAILABLE').count()