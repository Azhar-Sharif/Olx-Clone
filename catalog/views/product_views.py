from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from catalog.models.products import Product
from catalog.permissions import IsOwnerOrReadOnly
from catalog.serializers.serializers_product import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.select_related("category", "user").all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]

    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

    def perform_update(self, serializer):

        serializer.save(user=self.request.user)
