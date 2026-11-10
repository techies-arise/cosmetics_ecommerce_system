from django.contrib import admin
from .models import ProductImage

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'sort_order', 'created_at')
    list_filter = ('product__brand', 'created_at')
    search_fields = ('product__name', 'alt_text')
    ordering = ('product', 'sort_order')
