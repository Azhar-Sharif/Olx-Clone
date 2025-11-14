from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from catalog.models.products import Product
from catalog.permissions import IsOwnerOrReadOnly
from catalog.serializers.product import ProductSerializer
from core.utils.enums import SuccessMessages
from core.utils.response import api_response


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.select_related("category", "user").all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]

    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return api_response(
            True,
            message=SuccessMessages.PRODUCT_CREATED.value,
            data=response.data,
            status_code=response.status_code,
        )
