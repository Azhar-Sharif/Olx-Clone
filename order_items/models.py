from django.core.validators import MinValueValidator
from django.db import models


class OrderItem(models.Model):
    order = models.ForeignKey(
        "orders.Order", on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order", "product"], name="uniq_order_product"
            )
        ]
        ordering = ["order_id", "product_id"]

    def __str__(self):
        return f"{self.product_id} x {self.quantity} (₹{self.unit_price}) for order {self.order_id}"
