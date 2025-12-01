from rest_framework import serializers

from catalog.models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializes category data for list and detail endpoints."""

    class Meta:
        model = Category
        fields = ["id", "category_name"]
        read_only_fields = ["id"]
