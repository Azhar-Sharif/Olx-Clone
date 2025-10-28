from decimal import Decimal

from django.conf import settings
from django.db import models


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELED = "canceled", "Canceled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    order_date = models.DateTimeField(auto_now_add=True)

    # store all products here as JSON
    products = models.JSONField(default=list)

    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )
    shipping_address = models.TextField(blank=True, null=True)
    order_status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )

    class Meta:
        ordering = ["-order_date"]

    def __str__(self):
        return f"Order #{self.pk} by {self.user_id} [{self.order_status}]"

    def add_product(self, product_id, quantity, unit_price):
        """Add or update a product in the order"""
        for item in self.products:
            if item["product_id"] == product_id:
                item["quantity"] += quantity
                break
        else:
            self.products.append(
                {
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": str(unit_price),
                }
            )
        self.recompute_total(save=False)

    def recompute_total(self, save=True):
        """Calculate the total price based on products list"""
        total = sum(
            Decimal(item["unit_price"]) * item["quantity"]
            for item in self.products
        )
        self.total_amount = total
        if save:
            self.save(update_fields=["total_amount"])
        return total
