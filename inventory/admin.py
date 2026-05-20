from django.contrib import admin
from .models import EquipmentUnit, MaintenanceLog

# Register your models here.

@admin.register(EquipmentUnit)
class EquipmentUnitAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'equipment', 'status', 'last_calibration_date', 'next_maintenance_due')
    list_filter = ('status', 'equipment')
    search_fields = ('serial_number', 'internal_id')

@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ('equipment_unit', 'start_date', 'end_date', 'is_completed')
    list_filter = ('is_completed',)
    search_fields = ('equipment_unit__serial_number',)