from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")
    search_fields = ("category_name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product_name",
        "price",
        "category",
        "user",
        "created_at",
    )
    list_filter = ("category", "price")
    search_fields = ("product_name", "category")
    readonly_fields = ("created_at",)
