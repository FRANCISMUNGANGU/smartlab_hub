from django.contrib import admin
from .models import Transaction

# Register your models here.

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'transaction_reference', 'created_at', 'updated_at')
    list_filter = ('transaction_reference', 'created_at')
    search_fields = ('booking__user__username', 'booking__unit__serial_number')