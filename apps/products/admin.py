from django.contrib import admin
from .models import Products

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display=('name', 'brand', 'category', 'status', 'created_at')
    list_filter = ('status', 'brand', 'category', 'created_at')
    search_fields = ('name', 'brand', 'description')
    prepopulated_fields = {'slug': ('brand', 'name')}
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
