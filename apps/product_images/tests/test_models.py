from django.test import TestCase
from django.db.utils import IntegrityError
from apps.products.models import Category, Product
from apps.product_images.models import ProductImage

class ProductImageModelTestCase(TestCase):
    
    def setUp(self):
        """Arrange: Set up the parent category and product required for the image foreign key."""
        self.category = Category.objects.create(name="Makeup")
        self.product = Product.objects.create(
            category=self.category,
            name="Matte Liquid Lipstick",
            brand="Fenty Beauty"
        )

    def test_product_image_creation_and_forward_lookup(self):
        """Verify an image record successfully links to its parent product."""
        # Arrange
        image_url = "https://example.com/images/lipstick-red.jpg"
        alt_text = "Fenty Matte Lipstick in shade MVP"

        # Act
        product_image = ProductImage.objects.create(
            product=self.product,
            image_url=image_url,
            alt_text=alt_text,
            sort_order=1
        )

        # Assert
        self.assertEqual(product_image.product, self.product)
        self.assertEqual(product_image.image_url, image_url)
        self.assertEqual(product_image.alt_text, alt_text)
        self.assertEqual(product_image.sort_order, 1)

    def test_product_image_reverse_lookup(self):
        """Verify a product can access all its associated images via related_name."""
        # Arrange
        img_one = ProductImage.objects.create(
            product=self.product,
            image_url="https://example.com/front.jpg",
            sort_order=1
        )
        img_two = ProductImage.objects.create(
            product=self.product,
            image_url="https://example.com/swatch.jpg",
            sort_order=2
        )

        # Act
        product_images = self.product.images.all()

        # Assert
        self.assertEqual(product_images.count(), 2)
        self.assertIn(img_one, product_images)
        self.assertIn(img_two, product_images)

    def test_product_image_foreign_key_protection(self):
        """Ensure an image cannot be created without a valid parent product."""
        # Act & Assert
        with self.assertRaises(IntegrityError):
            ProductImage.objects.create(
                product_id=99999,  # Non-existent product ID
                image_url="https://example.com/orphan.jpg"
            )