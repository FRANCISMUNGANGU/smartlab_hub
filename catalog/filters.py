from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Equipment
from inventory.models import EquipmentUnit

class EquipmentFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="rental_price_per_day", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="rental_price_per_day", lookup_expr='lte')
    
    # Custom filters for date range
    available_from = filters.DateTimeFilter(method='filter_availability')
    available_to = filters.DateTimeFilter(method='filter_availability')

    class Meta:
        model = Equipment
        fields = ['category', 'brand', 'name']

    def filter_availability(self, queryset, name, value):
        # Grab both dates from the request data
        start = self.data.get('available_from')
        end = self.data.get('available_to')

        if not (start and end):
            return queryset

        # Logic: Keep Equipment only if it has >= 1 unit NOT booked/in maintenance
        # We use a subquery or a pre-filtered list of Equipment IDs
        available_equipment_ids = EquipmentUnit.objects.exclude(
            Q(status__in=['SOLD', 'DAMAGED']) |
            Q(bookings__start_date__lte=end, bookings__end_date__gte=start) |
            Q(maintenance_history__start_date__lte=end, maintenance_history__end_date__gte=start)
        ).values_list('equipment_id', flat=True).distinct()

        return queryset.filter(id__in=available_equipment_ids)