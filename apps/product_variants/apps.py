from django.apps import AppConfig


class ProductVariantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.product_variants'
    verbose_name = 'Product Variant'
    verbose_name_plural = 'Product Variants'
    label='product_variants'
