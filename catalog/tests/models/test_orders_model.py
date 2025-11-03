from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model

from catalog.models.orders import Order

User = get_user_model()


@pytest.mark.django_db
class TestOrderModel:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
        )

    def test_create_order_defaults(self, user):
        """Ensure an order is created with correct default values."""
        order = Order.objects.create(user=user)

        assert order.user == user
        assert order.total_amount == Decimal("0.00")
        assert order.order_status == Order.Status.PENDING
        assert order.products == []
        assert order.order_date is not None

    def test_add_product_new_item(self, user):
        """Adding a new product should add it to products list."""
        order = Order.objects.create(user=user)

        order.add_product(
            product_id=1, quantity=2, unit_price=Decimal("50.00")
        )

        assert len(order.products) == 1
        assert order.products[0]["product_id"] == 1
        assert order.products[0]["quantity"] == 2
        assert order.total_amount == Decimal("100.00")

    def test_add_product_existing_item_updates_quantity(self, user):
        """Adding an existing product should increase its quantity."""
        order = Order.objects.create(user=user)

        order.add_product(
            product_id=1, quantity=2, unit_price=Decimal("30.00")
        )
        order.add_product(
            product_id=1, quantity=3, unit_price=Decimal("30.00")
        )

        assert len(order.products) == 1
        assert order.products[0]["quantity"] == 5
        assert order.total_amount == Decimal("150.00")

    def test_recompute_total_manual(self, user):
        """Ensure recompute_total calculates sum correctly."""
        order = Order.objects.create(user=user)
        order.products = [
            {"product_id": 1, "quantity": 2, "unit_price": "40.00"},
            {"product_id": 2, "quantity": 3, "unit_price": "10.00"},
        ]

        total = order.recompute_total()

        assert total == Decimal("110.00")
        assert order.total_amount == Decimal("110.00")
