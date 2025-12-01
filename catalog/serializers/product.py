"""Product serializers.

Provides serialization and validation for product data.
"""

from decimal import Decimal

from rest_framework import serializers

from catalog.models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    """Serializes product data for list, detail, and write
    operations."""

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        help_text="Primary key of the product category",
    )

    category_name = serializers.ReadOnlyField(
        source="category.category_name",
        help_text="Category name",
    )

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    user_name = serializers.ReadOnlyField(
        source="user.username",
        help_text="Owner username",
    )

    product_img = serializers.ImageField(
        required=False,
        allow_null=True,
        help_text="Product image file",
    )

    product_img_url = serializers.SerializerMethodField(
        read_only=True,
        help_text="Full URL to the product image",
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "quantity",
            "description",
            "price",
            "product_img",
            "product_img_url",
            "created_at",
            "user",
            "user_name",
            "category",
            "category_name",
        ]
        read_only_fields = ["id", "created_at"]

    def get_product_img_url(self, obj):
        return obj.product_img.url if obj.product_img else None

    def validate_price(self, value: Decimal) -> Decimal:
        """Validates that the price is zero or positive."""
        if value < 0:
            raise serializers.ValidationError(
                "Price must be zero or positive.",
            )
        return value
