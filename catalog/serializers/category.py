from rest_framework import serializers

from catalog.models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer.

    Response (api_response wrapper) example:
    {
        "success": true,
        "message": "Category listed successfully",
        "data": [
            {
                "id": 1,
                "category_name": "Electronics"
            }
        ],
        "errors": null
    }
    """

    class Meta:
        model = Category
        fields = ["id", "category_name"]
        read_only_fields = ["id"]
