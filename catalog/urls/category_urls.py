from django.urls import path

from catalog.views.category_view import CategoryDetailView, CategoryListView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path(
        "categories/<int:pk>/",
        CategoryDetailView.as_view(),
        name="category-detail",
    ),
]
