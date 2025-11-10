from decimal import Decimal

from rest_framework import serializers

from catalog.models import Category, Product


class ProductSerializer(serializers.ModelSerializer):

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    category_name = serializers.ReadOnlyField(source="category.category_name")

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    user_name = serializers.ReadOnlyField(source="user.username")

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
            "user_name",
            "category",
            "category_name",
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
