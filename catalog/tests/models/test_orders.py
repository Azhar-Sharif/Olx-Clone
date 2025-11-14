from decimal import Decimal

import pytest
from faker import Faker

from catalog.models.orders import Order
from catalog.tests.factories.orders import OrderFactory

faker = Faker()


@pytest.mark.django_db
class TestOrderModel:
    def test_create_order_defaults(self):
        order = OrderFactory()

        assert order.user is not None
        assert order.total_amount == Decimal("0.00")
        assert order.order_status == Order.Status.PENDING
        assert order.products == []
        assert order.order_date is not None

    def test_add_product_new_item(self):
        order = OrderFactory()
        product_id = faker.pyint(min_value=1, max_value=10_000)
        quantity = faker.pyint(min_value=1, max_value=10)
        unit_price = Decimal(
            str(faker.pydecimal(left_digits=3, right_digits=2, positive=True))
        )

        order.add_product(
            product_id=product_id, quantity=quantity, unit_price=unit_price
        )

        assert len(order.products) == 1
        item = order.products[0]
        assert item["product_id"] == product_id
        assert item["quantity"] == quantity
        expected_total = unit_price * quantity
        assert order.total_amount == expected_total

    def test_add_product_existing_item_updates_quantity(self):
        order = OrderFactory()

        product_id = faker.pyint(min_value=1, max_value=10_000)
        q1 = faker.pyint(min_value=1, max_value=5)
        q2 = faker.pyint(min_value=1, max_value=5)
        unit_price = Decimal(
            str(faker.pydecimal(left_digits=3, right_digits=2, positive=True))
        )

        order.add_product(
            product_id=product_id, quantity=q1, unit_price=unit_price
        )
        order.add_product(
            product_id=product_id, quantity=q2, unit_price=unit_price
        )

        assert len(order.products) == 1
        item = order.products[0]
        assert item["product_id"] == product_id
        assert item["quantity"] == q1 + q2
        assert order.total_amount == unit_price * (q1 + q2)

    def test_recompute_total_manual(self):
        order = OrderFactory()

        p1_price = Decimal(
            str(faker.pydecimal(left_digits=3, right_digits=2, positive=True))
        )
        p2_price = Decimal(
            str(faker.pydecimal(left_digits=3, right_digits=2, positive=True))
        )
        p1_qty = faker.pyint(min_value=1, max_value=5)
        p2_qty = faker.pyint(min_value=1, max_value=5)

        order.products = [
            {
                "product_id": faker.pyint(min_value=1, max_value=10_000),
                "quantity": p1_qty,
                "unit_price": str(p1_price),
            },
            {
                "product_id": faker.pyint(min_value=1, max_value=10_000),
                "quantity": p2_qty,
                "unit_price": str(p2_price),
            },
        ]

        total = order.recompute_total()
        expected = p1_price * p1_qty + p2_price * p2_qty
        assert total == expected
        assert order.total_amount == expected
