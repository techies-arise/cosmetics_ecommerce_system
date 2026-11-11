from decimal import Decimal
from django.test import TestCase
from django.db.utils import IntegrityError
from apps.products.models import Category, Product
from apps.product_variants.models import ProductVariant

class ProductVariantModelTestCase(TestCase):
    
    def setUp(self):
        """Arrange: Set up the prerequisite category and product for our variants."""
        self.category = Category.objects.create(name="Foundation")
        self.product = Product.objects.create(
            category=self.category,
            name="Liquid Silk Foundation",
            brand="Glossier"
        )

    def test_product_variant_successful_creation(self):
        """Verify that a variant instantiates correctly with all fields and JSON attributes."""
        # --- ARRANGE ---
        sku_code = "GLOSS-SILK-IVORY-30ML"
        variant_title = "Ivory - 30ml"
        variant_price = Decimal("42.00")
        variant_attrs = {"shade": "Ivory", "size": "30ml", "hex": "#FFF4E0"}

        # --- ACT ---
        variant = ProductVariant.objects.create(
            product=self.product,
            sku=sku_code,
            variant_name=variant_title,
            price=variant_price,
            attributes=variant_attrs,
            is_active=True
        )

        # --- ASSERT ---
        self.assertEqual(variant.product, self.product)
        self.assertEqual(variant.sku, sku_code)
        self.assertEqual(variant.variant_name, variant_title)
        self.assertEqual(variant.price, variant_price)
        self.assertEqual(variant.attributes["shade"], "Ivory")
        self.assertTrue(variant.is_active)
        self.assertIsNotNone(variant.id)  # Confirm UUID is generated

    def test_product_variant_sku_uniqueness_constraint(self):
        """Ensure two variants cannot share the exact same SKU."""
        # --- ARRANGE ---
        ProductVariant.objects.create(
            product=self.product,
            sku="UNIQUE-SKU-123",
            variant_name="Shade A",
            price=Decimal("30.00")
        )

        # --- ACT & ASSERT ---
        with self.assertRaises(IntegrityError):
            ProductVariant.objects.create(
                product=self.product,
                sku="UNIQUE-SKU-123",  # Duplicate SKU attempt
                variant_name="Shade B",
                price=Decimal("35.00")
            )

    def test_product_variant_reverse_lookup(self):
        """Verify a product can fetch all its variants using related_name='variants'."""
        # --- ARRANGE ---
        variant_one = ProductVariant.objects.create(
            product=self.product, sku="SKU-001", variant_name="Small", price=Decimal("20.00")
        )
        variant_two = ProductVariant.objects.create(
            product=self.product, sku="SKU-002", variant_name="Large", price=Decimal("35.00")
        )

        # --- ACT ---
        associated_variants = self.product.variants.all()

        # --- ASSERT ---
        self.assertEqual(associated_variants.count(), 2)
        self.assertIn(variant_one, associated_variants)
        self.assertIn(variant_two, associated_variants)