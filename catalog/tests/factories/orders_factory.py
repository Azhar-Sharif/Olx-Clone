from decimal import Decimal

import factory
from factory import LazyFunction, SubFactory

from catalog.models.orders import Order
from users.tests.user_factory import UserFactory


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = SubFactory(UserFactory)
    order_status = Order.Status.PENDING
    shipping_address = None
    products = LazyFunction(list)
    total_amount = Decimal("0.00")
