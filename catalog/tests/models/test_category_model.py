import pytest

from catalog.models.category import Category


@pytest.mark.django_db
class TestCategoryModel:
    """Simple tests for Category model"""

    def test_create_category(self):
        """Test creating a category"""
        category = Category.objects.create(category_name="Electronics")
        assert category.category_name == "Electronics"
        assert str(category) == "Electronics"

    def test_category_name_unique(self):
        """category_name must be unique"""
        Category.objects.create(category_name="Books")

        with pytest.raises(Exception):
            Category.objects.create(category_name="Books")

    def test_ordering(self):
        """Categories should be ordered by category_name"""
        Category.objects.create(category_name="Zebras")
        Category.objects.create(category_name="Apples")
        Category.objects.create(category_name="Bananas")

        categories = Category.objects.all()
        names = [category.category_name for category in categories]
        assert names == ["Apples", "Bananas", "Zebras"]
