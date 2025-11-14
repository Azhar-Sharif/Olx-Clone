from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from catalog.models.products import Product
from catalog.permissions import IsOwnerOrReadOnly
from catalog.serializers.product import ProductSerializer
from core.utils.enums import SuccessMessages
from core.utils.logger import log_debug, log_error, log_info
from core.utils.response import api_response


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.select_related("category", "user").all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]

    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        log_info("Product create called", extra={"user_id": request.user.id})
        log_debug(
            "Product create payload",
            extra={
                "data": {
                    k: v
                    for k, v in request.data.items()
                    if k.lower() not in ("password", "token")
                }
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
