from django.test import TestCase
from django.db.utils import IntegrityError
from apps.products.models import Category, Product
from apps.product_variants.models import ProductVariant
from apps.inventories.models import Inventory

class InventoryModelTestCase(TestCase):
    
    def setUp(self):
        """Arrange: Set up parent category, product, and variant prerequisites for inventory testing."""
        self.category = Category.objects.create(
            name="Skincare",
            description="Facial care items"
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Hydrating Cream",
            brand="Neutrogena"
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku="NEUTRO-CREAM-50ML",
            price=24.99
        )

    def test_inventory_creation_and_defaults(self):
        """Verify inventory instantiates correctly linked to a product variant."""
        # Arrange & Act
        inventory = Inventory.objects.create(
            product_variant=self.variant,
            quantity_on_hand=100,
            quantity_reserved=10
        )

        # Assert
        self.assertEqual(inventory.product_variant, self.variant)
        self.assertEqual(inventory.quantity_on_hand, 100)
        self.assertEqual(inventory.quantity_reserved, 10)
        # Verify reverse lookup from variant to inventory works
        self.assertEqual(self.variant.inventory, inventory)

    def test_available_quantity_calculation(self):
        """Verify computed property accurately calculates on_hand minus reserved stock."""
        # Arrange
        inventory = Inventory(
            product_variant=self.variant,
            quantity_on_hand=75,
            quantity_reserved=25
        )

        # Act & Assert
        self.assertEqual(inventory.available_quantity, 50)

    def test_available_quantity_clamps_to_zero(self):
        """Ensure available quantity never displays a negative number if reservations exceed stock."""
        # Arrange
        inventory = Inventory(
            product_variant=self.variant,
            quantity_on_hand=10,
            quantity_reserved=15
        )

        # Act & Assert
        self.assertEqual(inventory.available_quantity, 0)

    def test_inventory_one_to_one_uniqueness_constraint(self):
        """Ensure a product variant cannot have more than one inventory tracking record."""
        # Arrange: Create the first inventory tracking row
        Inventory.objects.create(
            product_variant=self.variant,
            quantity_on_hand=50
        )

        # Act & Assert: Attempting to create a second inventory row for the same variant raises IntegrityError
        with self.assertRaises(IntegrityError):
            Inventory.objects.create(
                product_variant=self.variant,
                quantity_on_hand=30
            )

# docker compose exec web python manage.py test apps.inventories.tests.test_models --settings=config.settings.development