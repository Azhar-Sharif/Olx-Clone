from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


class Order(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
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

    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )
    shipping_address = models.TextField(blank=True, null=True)
    order_status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )

    class Meta:
        ordering = ["-order_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=Q(order_status="draft"),
                name="uniq_draft_order_per_user",
            ),
        ]

    def __str__(self):
        return f"Order #{self.pk} by {self.user_id} [{self.order_status}]"

    def recompute_total(self, save=True):
        total = sum(
            (item.unit_price * item.quantity for item in self.items.all()),
            start=Decimal("0.00"),
        )
        self.total_amount = total
        if save:
            self.save(update_fields=["total_amount"])
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(
        "orders.Order", on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        "catalog.Product", on_delete=models.PROTECT, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    # Unit price at the time the item is added
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
