from django.db import models
import uuid
from django.utils.text import slugify
from apps.categories.models import models

# products
#  id, category_id, name, slug, description, brand, status, timestamps.


class Products(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        ACTIVE = "ACTIVE", "Active"
        ARCHIVED = "ARCHIVED", "Archived"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Category Rel
    category = models.ForeignKey(
        "categories.Categories", 
        on_delete=models.PROTECT, 
        related_name="products", 
        db_index=True
    )
    # core fields
    name = models.CharField(
        max_length=255,
        db_index=True,
    )
    slug = models.CharField(max_length=300, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=150, db_index=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True
    )
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "products"
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.brand} - {self.name}"

    def save(self, *args, **kwargs):
        # Auto generate slug if not provided
        if not self.slug:
            base_slug = slugify(f"{self.brand}-{self.name}")
            slug = base_slug
            counter = 1
            # just incase it already exists
            while Product.object.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
            super().save(*args, **kwargs)
