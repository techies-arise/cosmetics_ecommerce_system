from django.db import models
import uuid
from apps.products.models import Product

# product_images
#  id, product_id, image_url, alt_text, sort_order. Actual image bytes live in object storage.


class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Product relationship
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="images",
        db_index=True,
    )
    # Core fields
    image_url = models.URLField(max_length=1024)
    alt_text = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Alternative Text for accessibility and SEO",
    )
    sort_order = models.PositiveIntegerField(
        default=0, db_index=True, help_text="Display order from smallest to largest"
    )
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "product_images"
        db_table = "product_images"
        verbose_name = "Product Image"
        verbose_name_plural = "product Images"
        ordering = ["sort_order", "created_at"]

    def __str__(self):
        return f"Image for {self.Products.name} (Order:{self.sort_order})"
