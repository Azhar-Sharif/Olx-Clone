from rest_framework import serializers

from catalog.models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "category_name"]
        read_only_fields = ["id"]
