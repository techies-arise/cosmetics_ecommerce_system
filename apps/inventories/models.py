from django.db import models
import uuid
from apps.product_variants.models import  ProductVariant

# inventory
#  id, variant_id (unique), quantity_on_hand, quantity_reserved, updated_at. Available = on_hand − reserved.
class Inventory(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        db_index=True
    )
    product_variant = models.ForeignKey(
        'product_variants.ProductVariant',
        on_delete=models.CASCADE,
        related_name='variant'
    )
    # core fields
    quantity_on_hand = models.PositiveIntegerField(default=0)
    quantity_reserved = models.PositiveIntegerField(default=0)
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label='inventories'
        db_table='inventories'
        verbose_name='Inventory'
        verbose_name_plural='Inventories'
    def __str__(self):
        return f"{self.product_variant} — Available: {self.available_quantity}"

    @property
    def available_quantity(self):
        """Computed property implementing: Available = on_hand - reserved"""
        return max(0, self.quantity_on_hand - self.quantity_reserved)
