from django.contrib import admin
from .models import Inventory

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product_variant', 'quantity_on_hand','quantity_reserved', 'created_at')
    search_fields = ('product_variant',)
    list_filter = ('product_variant', 'created_at')