from django.test import TestCase
from django.db.utils import IntegrityError
from apps.products.models import Category, Product
from apps.product_variants.models import ProductVariant
from apps.inventory_transactions.models import InventoryTransaction

class InventoryTransactionModelTestCase(TestCase):
    
    def setUp(self):
        """Arrange: Set up parent product hierarchy for audit logging."""
        self.category = Category.objects.create(name="Fragrance")
        self.product = Product.objects.create(
            category=self.category,
            name="Eau de Parfum",
            brand="Chanel"
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku="CHANEL-EDP-100ML",
            price=135.00
        )

    def test_restock_transaction_creation(self):
        """Verify that a restock transaction records positive stock additions correctly."""
        # Act
        transaction = InventoryTransaction.objects.create(
            product_variant=self.variant,
            transaction_type=InventoryTransaction.TransactionType.RESTOCK,
            quantity_change=25,
            reference="Supplier delivery PO-9921"
        )

        # Assert
        self.assertEqual(transaction.product_variant, self.variant)
        self.assertEqual(transaction.transaction_type, InventoryTransaction.TransactionType.RESTOCK)
        self.assertEqual(transaction.quantity_change, 25)
        self.assertEqual(transaction.reference, "Supplier delivery PO-9921")
        self.assertIsNotNone(transaction.created_at)

    def test_sale_deduction_transaction_creation(self):
        """Verify that a sale transaction correctly logs negative inventory decrements."""
        # Act
        transaction = InventoryTransaction.objects.create(
            product_variant=self.variant,
            transaction_type=InventoryTransaction.TransactionType.SALE,
            quantity_change=-2,
            reference="Order #ORD-88321"
        )

        # Assert
        self.assertEqual(transaction.transaction_type, InventoryTransaction.TransactionType.SALE)
        self.assertEqual(transaction.quantity_change, -2)
        self.assertIn("ORD-88321", transaction.reference)

    def test_transaction_foreign_key_protection(self):
        """Ensure an audit log transaction cannot exist without a valid product variant reference."""
        with self.assertRaises(IntegrityError):
            InventoryTransaction.objects.create(
                product_variant_id=99999,  # Invalid foreign key
                transaction_type=InventoryTransaction.TransactionType.ADJUSTMENT,
                quantity_change=10
            )