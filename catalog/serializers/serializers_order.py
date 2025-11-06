from rest_framework import serializers

from catalog.models import Order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "order_date",
            "products",
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
        ]
