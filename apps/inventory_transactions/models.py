from django.db import models
import uuid
from apps.product_variants.models import ProductVariant

# inventory_transactions
#  id, variant_id, quantity_change, transaction_type, reference_id, reason, created_at. Stock movement audit
# trail.
class InventoryTransaction(models.Model):
    class TransactionType(models.TextChoices):
        RESTOCK = "RESTOCK","Restock"
        SALE = "SALE", "Sale"
        RETURN = "RETURN", "Customer Return"
        DAMAGE = "DAMAGE", "Damaged / Write-off"
        ADJUSTMENT = "ADJUSTMENT", "Manual Audit Adjustment"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
        )
    product_variant = models.OneToOneField(
        'product_variants.ProductVariant',
        on_delete=models.PROTECT,
        related_name='inventory_transaction'
        )
    quantity_change = models.IntegerField(
        help_text="Positive for stock addition,negative for stock reduction."
    )
    transaction_type = models.CharField(
        max_length=30,
        choices=TransactionType.choices,
        default=TransactionType.SALE,
        db_index=True
        )
    reference_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
        )
    reason = models.CharField(
        max_length=255,
        blank=True,
        null=True
        )
    # timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label='inventory_transactions'
        db_table='inventory_transactions'
        verbose_name='Inventory Transaction'
        verbose_name_plural='Inventory Transactions'
        ordering=['-created_at']
    def __str__(self):
        sign = "+" if self.quantity_change > 0 else ""
        return f"{self.product_variant} | {self.get_transaction_type_display()} ({sign}{self.quantity_change})"
