from django.test import TestCase
from django.db.utils import IntegrityError
from apps.products.models import Product
from apps.categories.models import Category


class ProductModelTestCase(TestCase):

    def setUp(self):
        """Global Arrange phase: Set up shared parent category data for all tests."""
        self.category = Category.objects.create(
            name="Makeup", description="Cosmetics for face and eyes"
        )

    def test_product_creation_defaults(self):
        """Verify that a product saves correctly with expected default statuses."""
        # Arrange
        product_name = "Matte Lipstick"
        product_brand = "Ruby Woo"

        # Act
        product = Product.objects.create(
            category=self.category, name=product_name, brand=product_brand
        )

        # Assert
        self.assertEqual(product.name, product_name)
        self.assertEqual(product.brand, product_brand)
        self.assertEqual(
            product.status, Product.Status.DRAFT
        )  # Verifying default status choice
        self.assertEqual(str(product), f"{product_brand} - {product_name}")

    def test_product_auto_slug_generation(self):
        """Verify that saving a product automatically compiles a clean brand-name slug."""
        # Arrange & Act
        product = Product.objects.create(
            category=self.category,
            name="Liquid Foundation",
            brand="Fenty Beauty",
            status=Product.Status.ACTIVE,
        )

        # Assert
        self.assertEqual(product.slug, "fenty-beauty-liquid-foundation")

    def test_product_slug_collision_increment(self):
        """Verify that duplicate brand/name combinations safely generate unique, incremented slugs."""
        # Arrange: Create the initial product
        Product.objects.create(
            category=self.category, name="Liquid Foundation", brand="Fenty Beauty"
        )

        # Act: Create a second product with the exact same brand and name
        duplicate_product = Product.objects.create(
            category=self.category, name="Liquid Foundation", brand="Fenty Beauty"
        )

        # Assert: The second product gets an automated numeric suffix
        self.assertEqual(duplicate_product.slug, "fenty-beauty-liquid-foundation-1")

    def test_product_category_protect_constraint(self):
        """Verify that deleting a category containing active products is blocked (PROTECT)."""
        # Arrange
        Product.objects.create(
            category=self.category, name="Setting Spray", brand="Urban Decay"
        )

        # Act & Assert: Attempting deletion should raise an IntegrityError
        with self.assertRaises(IntegrityError):
            self.category.delete()
