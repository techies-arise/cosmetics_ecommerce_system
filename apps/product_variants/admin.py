from django.contrib import admin
from .models import ProductVariant

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product','sku','variant_name','price','created_at')
    search_fields = ('sku', 'product','variant_name')
    list_filter = ('price', 'product')
