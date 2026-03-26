"""Product API views.


Expose CRUD endpoints for products using a ModelViewSet and the
api_response wrapper.
"""

from drf_spectacular.utils import extend_schema_view
from rest_framework import status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from catalog.models.products import Product
from catalog.permissions import IsOwnerOrReadOnly
from catalog.serializers.product import ProductSerializer
from core.utils.enums import ErrorMessages, SuccessMessages
from core.utils.logger import log_debug, log_error, log_info
from core.utils.response import api_response
from docs.catalog.docs_products import (
    product_create_schema,
    product_destroy_schema,
    product_list_schema,
    product_partial_update_schema,
    product_retrieve_schema,
    product_update_schema,
)


@extend_schema_view(
    list=product_list_schema,
    retrieve=product_retrieve_schema,
    create=product_create_schema,
    update=product_update_schema,
    partial_update=product_partial_update_schema,
    destroy=product_destroy_schema,
)
class ProductViewSet(viewsets.ModelViewSet):
    """Provides CRUD endpoints for products.

    Responses are wrapped using the api_response helper, and only the
    owner can modify or delete products.
    """

    queryset = Product.objects.select_related("category", "user").all()
    serializer_class = ProductSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        """Save a new product instance with the current user as
        owner.
        """
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):  # noqa: A003
        """List products and wrap response in api_response."""
        log_info(
            "Product list called",
            extra={"user_id": getattr(request.user, "id", None)},
        )
        response = super().list(request, *args, **kwargs)
        return api_response(
            True,
            message=SuccessMessages.PRODUCTS_LISTED.value,
            data=response.data,
            status_code=response.status_code,
        )

    def retrieve(self, request, *args, **kwargs):
        log_info(
            "Product retrieve called",
            extra={"user_id": getattr(request.user, "id", None)},
        )
        response = super().retrieve(request, *args, **kwargs)
        return api_response(
            True,
            message=SuccessMessages.PRODUCT_RETRIEVED.value,
            data=response.data,
            status_code=response.status_code,
        )

    def create(self, request, *args, **kwargs):
        """Create a product and return a wrapped custom API response."""
        if not request.user or not request.user.is_authenticated:
            return api_response(
                False,
                message=ErrorMessages.AUTH_REQUIRED.value,
                data=None,
                errors={
                    "detail": "Authentication credentials were not provided.",
                },
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        log_info("Product create called", extra={"user_id": request.user.id})
        log_debug(
            "Product create payload",
            extra={
                "data": {
                    k: v
                    for k, v in request.data.items()
                    if k.lower() not in ("password", "token")
                },
            },
        )
        try:
            response = super().create(request, *args, **kwargs)
            log_info(
                "Product created",
                extra={
                    "product_id": response.data.get("id"),
                    "user_id": request.user.id,
                },
            )
            return api_response(
                True,
                message=SuccessMessages.PRODUCT_CREATED.value,
                data=response.data,
                status_code=response.status_code,
            )
        except Exception as exc:
            log_error("Product create failed", extra={"error": str(exc)})
            raise

    def update(self, request, *args, **kwargs):
        """Update a product and wrap response in api_response."""
        log_info(
            "Product update called",
            extra={"user_id": getattr(request.user, "id", None)},
        )
        response = super().update(request, *args, **kwargs)
        log_info(
            "Product updated",
            extra={
                "product_id": response.data.get("id"),
                "user_id": getattr(request.user, "id", None),
            },
        )
        return api_response(
            True,
            message=SuccessMessages.PRODUCT_UPDATED.value,
            data=response.data,
            status_code=response.status_code,
        )

    def partial_update(self, request, *args, **kwargs):
        log_info(
            "Product partial update called",
            extra={"user_id": getattr(request.user, "id", None)},
        )
        response = super().partial_update(request, *args, **kwargs)
        log_info(
            "Product partially updated",
            extra={
                "product_id": response.data.get("id"),
                "user_id": getattr(request.user, "id", None),
            },
        )
        return api_response(
            True,
            message=SuccessMessages.PRODUCT_UPDATED.value,
            data=response.data,
            status_code=response.status_code,
        )

    def destroy(self, request, *args, **kwargs):
        """Delete a product and wrap response in api_response."""
        product = self.get_object()
        product_id = product.id
        user_id = getattr(request.user, "id", None)
        log_info(
            "Product delete called",
            extra={"product_id": product_id, "user_id": user_id},
        )

        super().destroy(request, *args, **kwargs)

        log_info(
            "Product deleted",
            extra={"product_id": product_id, "user_id": user_id},
        )
        return api_response(
            True,
            message=SuccessMessages.PRODUCT_DELETED.value,
            data=None,
            status_code=status.HTTP_200_OK,
        )
