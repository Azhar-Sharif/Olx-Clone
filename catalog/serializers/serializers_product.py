from decimal import Decimal

from rest_framework import serializers

from catalog.models import Category, Product
from catalog.serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    category_detail = CategorySerializer(source="category", read_only=True)

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    product_img = serializers.ImageField(required=False, allow_null=True)

    product_img_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "description",
            "price",
            "product_img",
            "product_img_url",
            "created_at",
            "user",
            "category",
            "category_detail",
        ]
        read_only_fields = ["id", "created_at"]

    def get_product_img_url(self, obj):
        return obj.product_img.url if obj.product_img else None

    def validate_price(self, value: Decimal) -> Decimal:
        if value < 0:
            raise serializers.ValidationError(
                "Price must be zero or positive."
            )
        return value
