from rest_framework import generics, permissions

from catalog.models.category import Category
from catalog.serializers import CategorySerializer
from core.utils.enums import SuccessMessages
from core.utils.response import api_response


class CategoryListView(generics.ListAPIView):
    """
    List all categories.

    Authentication: Not required
    Permissions: Public

    Response example:
    {
        "success": true,
        "message": "Categories retrieved successfully",
        "data": [
            {"id": 1, "category_name": "Electronics"},
            {"id": 2, "category_name": "Books"}
        ],
        "errors": null
    }
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return api_response(
            True,
            message=SuccessMessages.CATEGORY_LISTED.value,
            data=response.data,
        )


class CategoryDetailView(generics.RetrieveAPIView):
    """
    Retrieve a category by ID.

    Authentication: Not required
    Permissions: Public

    Response example:
    {
        "success": true,
        "message": "Category retrieved successfully",
        "data": {"id": 1, "category_name": "Electronics"},
        "errors": null
    }
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return api_response(
            True,
            message=SuccessMessages.CATEGORY_RETRIEVED.value,
            data=response.data,
        )
