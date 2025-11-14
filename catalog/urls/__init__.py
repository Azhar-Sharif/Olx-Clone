from django.urls import include, path

urlpatterns = [
    path("", include("catalog.urls.category")),
    path("", include("catalog.urls.order")),
    path("", include("catalog.urls.products")),
]
