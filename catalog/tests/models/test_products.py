from decimal import Decimal

import pytest
from django.db.models.deletion import ProtectedError
from freezegun import freeze_time

from catalog.models.products import Product
from catalog.tests.factories.category import CategoryFactory
from catalog.tests.factories.products import ProductFactory
from users.tests.user_factory import UserFactory


@pytest.mark.django_db
class TestProductModel:

    def test_create_product_minimal(self):
        category = CategoryFactory(category_name="Electronics")
        product = ProductFactory(
            product_name="Phone",
            price=Decimal("499.99"),
            category=category,
            user=None,
            product_img=None,
            description="",
        )

        assert product.id is not None
        assert product.product_name == "Phone"
        assert product.description == ""
        assert product.price == Decimal("499.99")
        assert not product.product_img
        assert product.user is None
        assert product.category == category
        assert str(product) == "Phone"

    def test_create_product_with_user(self):
        category = CategoryFactory(category_name="Books")
        user = UserFactory(username="alice")
        product = ProductFactory(
            product_name="Novel",
            price=Decimal("19.99"),
            category=category,
            user=user,
            description="A great read",
        )

        assert product.user == user
        user.delete()
        product.refresh_from_db()
        assert product.user is None

    def test_category_delete_is_protected(self):
        """Category is protected; cannot delete while products exist"""
        category = CategoryFactory(category_name="Gadgets")
        ProductFactory(
            product_name="Smartwatch",
            price=Decimal("149.00"),
            category=category,
        )

        with pytest.raises(ProtectedError):
            category.delete()

    def test_related_names(self):
        category = CategoryFactory(category_name="Home")
        user = UserFactory(username="bob")

        ProductFactory(
            product_name="Vacuum",
            price=Decimal("89.50"),
            category=category,
            user=user,
        )
        ProductFactory(
            product_name="Mop",
            price=Decimal("12.00"),
            category=category,
            user=user,
        )

        assert user.products.count() == 2
        assert category.products.count() == 2

    def test_ordering_by_created_at_desc(self):
        """Default ordering should return newest first (-created_at)"""
        category = CategoryFactory(category_name="Office")

        with freeze_time("2025-01-01 10:00:00"):
            ProductFactory(
                product_name="Pen", price=Decimal("1.00"), category=category
            )
        with freeze_time("2025-01-01 10:00:01"):
            ProductFactory(
                product_name="Notebook",
                price=Decimal("2.50"),
                category=category,
            )
        with freeze_time("2025-01-01 10:00:02"):
            ProductFactory(
                product_name="Stapler",
                price=Decimal("5.75"),
                category=category,
            )

        products = list(Product.objects.all())
        assert [p.product_name for p in products] == [
            "Stapler",
            "Notebook",
            "Pen",
        ]

    def test_price_precision(self):
        """Price should store decimal with 2 places"""
        product = ProductFactory(product_name="Puzzle", price=Decimal("10.00"))
        assert product.price == Decimal("10.00")
