from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from catalog.models.orders import Order

User = get_user_model()


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
        )

    def test_create_order_defaults(self):
        """Ensure an order is created with correct default values."""
        order = Order.objects.create(user=self.user)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total_amount, Decimal("0.00"))
        self.assertEqual(order.order_status, Order.Status.PENDING)
        self.assertEqual(order.products, [])
        self.assertIsNotNone(order.order_date)

    def test_add_product_new_item(self):
        """Adding a new product should add it to products list."""
        order = Order.objects.create(user=self.user)
        order.add_product(
            product_id=1, quantity=2, unit_price=Decimal("50.00")
        )
        self.assertEqual(len(order.products), 1)
        self.assertEqual(order.products[0]["product_id"], 1)
        self.assertEqual(order.products[0]["quantity"], 2)
        self.assertEqual(order.total_amount, Decimal("100.00"))

    def test_add_product_existing_item_updates_quantity(self):
        """Adding an existing product should increase its quantity."""
        order = Order.objects.create(user=self.user)
        order.add_product(
            product_id=1, quantity=2, unit_price=Decimal("30.00")
        )
        order.add_product(
            product_id=1, quantity=3, unit_price=Decimal("30.00")
        )

        self.assertEqual(len(order.products), 1)
        self.assertEqual(order.products[0]["quantity"], 5)
        self.assertEqual(order.total_amount, Decimal("150.00"))

    def test_recompute_total_manual(self):
        """Ensure recompute_total calculates sum correctly."""
        order = Order.objects.create(user=self.user)
        order.products = [
            {"product_id": 1, "quantity": 2, "unit_price": "40.00"},
            {"product_id": 2, "quantity": 3, "unit_price": "10.00"},
        ]
        total = order.recompute_total()
        self.assertEqual(total, Decimal("110.00"))
        self.assertEqual(order.total_amount, Decimal("110.00"))

    def test_str_method_output(self):
        """Ensure __str__ returns the correct format."""
        order = Order.objects.create(user=self.user)
        result = str(order)
        self.assertIn(f"Order #{order.pk}", result)
        self.assertIn("pending", result)
