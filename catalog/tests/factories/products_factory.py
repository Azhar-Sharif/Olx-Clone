from decimal import Decimal

import factory
from factory import SubFactory

from catalog.models.products import Product
from catalog.tests.factories.category_factory import CategoryFactory


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    product_name = factory.Faker("sentence", nb_words=2)
    description = ""
    price = factory.LazyFunction(
        lambda: Decimal(
            factory.Faker(
                "pydecimal", left_digits=3, right_digits=2, positive=True
            ).generate({})
        )
    )
    product_img = None
    user = None
    category = SubFactory(CategoryFactory)
