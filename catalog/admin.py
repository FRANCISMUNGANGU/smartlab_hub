from django.contrib import admin
from .models import Category, Equipment

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'model_number', 'category', 'vendor', 'rental_price_per_day', 'purchase_price')
    list_filter = ('category', 'vendor')
    search_fields = ('name', 'brand', 'model_number')