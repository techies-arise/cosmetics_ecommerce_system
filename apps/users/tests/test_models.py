from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()  # Always use get_user_model() for custom auth models

class UserModelTestCase(TestCase):

    def test_create_standard_customer_success(self):
        """Verify that a standard customer user is created with correct defaults, field values, and hashed passwords."""
        # --- ARRANGE ---
        email = "customer@example.com"
        password = "StrongPassword123!"
        first_name = "Jane"
        last_name = "Doe"
        phone = "+254712345678"

        # --- ACT ---
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )

        # --- ASSERT ---
        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.phone, phone)
        self.assertEqual(user.role, User.Role.CUSTOMER)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        # Verify password security and verification method
        self.assertNotEqual(user.password, password)
        self.assertTrue(user.check_password(password))
        self.assertIsNotNone(user.id)  # Confirm UUID is generated

    def test_email_normalization(self):
        """Verify that uppercase letters in the email domain are correctly normalized."""
        # --- ARRANGE ---
        raw_email = "Test.User@EXAMPLE.com"

        # --- ACT ---
        user = User.objects.create_user(
            email=raw_email,
            password="Password123!",
            first_name="Test",
            last_name="User"
        )

        # --- ASSERT ---
        self.assertEqual(user.email, "Test.User@example.com")

    def test_create_superuser_success(self):
        """Verify that superuser creation sets administrative flags and admin role properly."""
        # --- ARRANGE ---
        email = "admin@cosmetics.com"
        password = "AdminPassword123!"

        # --- ACT ---
        admin_user = User.objects.create_superuser(
            email=email,
            password=password,
            first_name="Super",
            last_name="Admin"
        )

        # --- ASSERT ---
        self.assertEqual(admin_user.role, User.Role.ADMIN)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.check_password(password))

    def test_user_email_uniqueness_constraint(self):
        """Ensure that two users cannot be created with the exact same email address."""
        # --- ARRANGE ---
        User.objects.create_user(
            email="unique@example.com",
            password="Password123!",
            first_name="First",
            last_name="User"
        )

        # --- ACT & ASSERT ---
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="unique@example.com",  # Duplicate email attempt
                password="DifferentPassword456!",
                first_name="Second",
                last_name="User"
            )