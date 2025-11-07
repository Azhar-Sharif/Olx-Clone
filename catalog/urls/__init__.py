from django.urls import include, path

urlpatterns = [
    path("", include("catalog.urls.category_urls")),
    path("", include("catalog.urls.order_urls")),
    path("", include("catalog.urls.products_url")),
]
