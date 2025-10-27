from django.conf import settings
from django.db import models


class Category(models.Model):
    category_name = models.charfield(max_length=120, unique=True)

    class Meta:
        ordering = ["category_name"]

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_img = models.ImageField(uploads_to="products/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )

    category = models.ForeignKey(
        "catalog.Category", on_delete=models.PROTECT, related_name="products"
    )

    class Meta:
        indexes = [
            models.Index(fields=["product_name"]),
            models.Index(fields=["-created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return self.product_name
