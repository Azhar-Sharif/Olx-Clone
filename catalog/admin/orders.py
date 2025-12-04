from decimal import Decimal

from django.contrib import admin
from django.utils.html import format_html, format_html_join

from catalog.models.orders import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "order_date", "order_status", "total_amount")
    list_filter = ("order_status", "order_date")
    search_fields = ("user__username", "user__email")
    ordering = ("-order_date",)

    readonly_fields = ("order_date", "total_amount", "products_display")

    fieldsets = (
        (None, {"fields": ("user", "order_status", "shipping_address")}),
        ("Computed", {"fields": ("order_date", "total_amount")}),
        ("Products", {"fields": ("products_display",)}),
    )

    def products_display(self, obj):
        if not getattr(obj, "products", None):
            return "(no products)"

        def _item_tuple(item):
            pid = item.get("product_id")
            qty = item.get("quantity")
            try:
                price = Decimal(item.get("unit_price"))
            except Exception:
                price = item.get("unit_price")
            price_str = (
                f"{price:.2f}" if isinstance(price, Decimal) else str(price)
            )
            return (pid, qty, price_str)

        return format_html(
            "<ul>{}</ul>",
            format_html_join(
                "",
                "<li>Product ID: {} | Qty: {} | Price: {}</li>",
                (_item_tuple(it) for it in obj.products),
            ),
        )

    products_display.short_description = "Products"
