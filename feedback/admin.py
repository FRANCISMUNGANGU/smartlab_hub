from django.contrib import admin
from .models import IncidentReport, Feedback
# Register your models here.
@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ('equipment_unit', 'target_user', 'incident_type', 'description', 'reported_at')
    list_filter = ('incident_type', 'reported_at')
    search_fields = ('equipment_unit__serial_number', 'target_user__username')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'comment', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username',)