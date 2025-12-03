from django.contrib import admin

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
        lines = []
        for it in obj.products:
            pid = it.get("product_id")
            qty = it.get("quantity")
            price = it.get("unit_price")
            lines.append(f"Product ID: {pid} | Qty: {qty} | Price: {price}")
        return "\n".join(lines)

    products_display.short_description = "Products"
