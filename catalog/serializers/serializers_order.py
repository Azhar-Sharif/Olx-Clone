from rest_framework import serializers

from catalog.models import Order, Product


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    products = serializers.JSONField(read_only=True)
    products_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "order_date",
            "products",
            "products_ids",
            "total_amount",
            "shipping_address",
            "order_status",
        ]
        read_only_fields = [
            "id",
            "user",
            "order_date",
            "total_amount",
            "order_status",
            "products",
        ]

    def create(self, validated_data):
        product_ids = validated_data.pop("products_ids")
        user = self.context["request"].user

        products = Product.objects.filter(id__in=[p.id for p in product_ids])
        products_list = [
            {
                "product_id": p.id,
                "product_name": p.product_name,
                "quantity": 1,
                "unit_price": str(p.price),
            }
            for p in products
        ]

        order = Order.objects.create(
            user=user,
            products=products_list,
            shipping_address=validated_data.get("shipping_address"),
        )
        order.recompute_total()
        return order
