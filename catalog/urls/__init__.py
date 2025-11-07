from django.urls import include, path

from catalog.urls.category_urls import urlpatterns
from catalog.urls.order_urls import urlpatterns
from catalog.urls.products_url import urlpatterns

urlpatterns = [
    path("", include("catalog.urls.category_urls")),
    path("", include("catalog.urls.order_urls")),
    path("", include("catalog.urls.products_url")),
]
