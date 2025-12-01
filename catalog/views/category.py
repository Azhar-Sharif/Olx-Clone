"""
Catalog category API views.

Provides list and detail endpoints for categories
with a costume api_response."""

from rest_framework import generics, permissions

from catalog.models.category import Category
from catalog.serializers import CategorySerializer
from core.utils.enums import SuccessMessages
from core.utils.response import api_response


class CategoryListView(generics.ListAPIView):
    """Lists all categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):  # noqa: A003
        """Returns a costume API response with the category list."""
        response = super().list(request, *args, **kwargs)
        return api_response(
            True,
            message=SuccessMessages.CATEGORY_LISTED.value,
            data=response.data,
        )


class CategoryDetailView(generics.RetrieveAPIView):
    """Retrieves a single category by its identifier."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        """Returns a costume API response with the category details."""
        response = super().retrieve(request, *args, **kwargs)
        return api_response(
            True,
            message=SuccessMessages.CATEGORY_RETRIEVED.value,
            data=response.data,
        )
