from rest_framework import serializers
from .models import EquipmentUnit, MaintenanceLog
from catalog.models import Equipment


class EquipmentMinimalSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Equipment
        fields = ['id', 'name', 'brand', 'model_number', 'image']

class EquipmentUnitSerializer(serializers.ModelSerializer):
    equipment = EquipmentMinimalSerializer(read_only=True)

    class Meta:
        model = EquipmentUnit
        fields = [
            'id', 'equipment', 'serial_number', 'internal_id', 'status', 'last_calibration_date', 'next_maintenance_due']
        
        extra_kwargs = {'equipment': {'write_only': True}}

        def get_next_maintenance_due(self, obj):
            if obj.next_maintenance_due:
                from django.utils import timezone
                delta = obj.next_maintenance_due - timezone.now().date()
                return delta.days
            return None
        

class MaintenanceLogSerializer(serializers.ModelSerializer):
    equipment_unit = serializers.PrimaryKeyRelatedField(queryset=EquipmentUnit.objects.all())
    equipment_name = serializers.ReadOnlyField(source='equipment_unit.equipment.name')

    class Meta:
        model = MaintenanceLog
        fields = ['id', 'equipment_unit', 'equipment_name', 'performed_by', 'maintenance_type', 'description', 'performed_at']
        read_only_fields = ['id', 'performed_at']