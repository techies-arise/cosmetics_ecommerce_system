from django.contrib import admin 
from .models import InventoryTransaction
@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'product_variant', 'transaction_type', 'quantity_change', 'reference_id')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('product_variant__sku', 'reference_id', 'reason')
    ordering = ('-created_at',)
    
    # Enterprise security: Audit logs cannot be edited or created manually via UI
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
