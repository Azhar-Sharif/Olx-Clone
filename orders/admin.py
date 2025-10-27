from django.contrib import admin

from order_items.models import OrderItem

from .models import Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "order_date", "order_status", "total_amount")
    list_filter = ("order_status", "order_date")
    search_fields = ("user__username", "user__email")
    ordering = ("-order_date",)
    inlines = [OrderItemInline]
