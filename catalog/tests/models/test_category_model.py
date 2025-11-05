import pytest
from django.db import IntegrityError

from catalog.models.category import Category
from catalog.tests.factories.category_factory import CategoryFactory


@pytest.mark.django_db
class TestCategoryModel:
    """Simple tests for Category model using Factory Boy"""

    def test_create_category(self):
        """Test creating a category"""
        category = CategoryFactory(category_name="Electronics")
        assert category.category_name == "Electronics"
        assert str(category) == "Electronics"

    def test_category_name_unique(self):
        """category_name must be unique"""
        CategoryFactory(category_name="Books")

        with pytest.raises(IntegrityError):
            CategoryFactory(category_name="Books")

    def test_ordering(self):
        """Categories should be ordered by category_name"""
        CategoryFactory(category_name="Zebras")
        CategoryFactory(category_name="Apples")
        CategoryFactory(category_name="Bananas")

        categories = Category.objects.all()
        names = [c.category_name for c in categories]
        assert names == ["Apples", "Bananas", "Zebras"]
