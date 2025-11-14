from django.db import transaction
from django.db.models import F
from rest_framework import serializers

from catalog.models import Order, Product


class OrderProductInputSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    quantity = serializers.IntegerField(min_value=1)


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    products = serializers.JSONField(read_only=True)
    products_data = OrderProductInputSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "order_date",
            "products",
            "products_data",
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
        products_data = validated_data.pop("products_data")
        user = self.context["request"].user

        products_list = []

        with transaction.atomic():
            for item in products_data:
                product = item["product_id"]
                quantity = item["quantity"]

                if product.quantity < quantity:
                    raise serializers.ValidationError(
                        {
                            f"Inventory check failed: The quantity requested for product {product.id} is not available."
                        }
                    )

                products_list.append(
                    {
                        "product_id": product.id,
                        "product_name": product.product_name,
                        "quantity": quantity,
                        "unit_price": str(product.price),
                    }
                )

                Product.objects.filter(pk=product.pk).update(
                    quantity=F("quantity") - quantity
                )

            order = Order.objects.create(
                user=user,
                products=products_list,
                shipping_address=validated_data["shipping_address"],
            )
            order.recompute_total()

        return order
