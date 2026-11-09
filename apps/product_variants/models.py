from django.db import models
import uuid
from apps.products.models import models
from django.core.validators import MinValueValidator


# product_variants
#  id, product_id, SKU, variant_name, price, attributes JSON, is_active. Each sellable size/shade/form has its
# own SKU.
class ProductVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Foreign key back to the parent product
    product = models.ForeignKey(
        "products.Products", on_delete=models.CASCADE, related_name="variants"
    )
    # Clean, searchable unique identifier for every sellable stock keeping unit
    sku = models.CharField("SKU", max_length=50, unique=True, db_index=True)
    # e.g., "Travel Size - 30ml"
    variant_name = models.CharField(max_length=255)
    # Price specific to this variant, protected against negative numbers
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    #  describing the product(e.g., {"shade": "Ivory", "size": "30ml", "hex": "#FFF4E0"})
    attributes = models.JSONField(default=dict, blank=True)
    # Soft flag to toggle variant availability without deleting data
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "product_variants"
        verbose_name = "Product Variants"
        verbose_name = "Product Variants"
        # Prevent duplicate names under the same product
        unique_together = ("product", "variant_name")

    def __str__(self):
        return f"{self.product.name} - {self.variant_name} ({self.sku})"
