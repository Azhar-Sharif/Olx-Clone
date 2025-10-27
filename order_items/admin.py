from django.contrib import admin

from .models import OrderItem


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "unit_price")
    list_filter = ("order", "product")
    search_fields = ("order__id", "product__product_name")
    ordering = ("order",)
