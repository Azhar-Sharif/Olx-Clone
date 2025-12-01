"""Order API views.

Exposes endpoints for listing, retrieving, creating, updating, and
canceling orders for the authenticated owner using the api_response
wrapper.
"""

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, viewsets

from catalog.models import Order
from catalog.permissions import IsOwnerOnly
from catalog.serializers import OrderSerializer
from core.utils.enums import SuccessMessages
from core.utils.logger import log_debug, log_error, log_info
from core.utils.response import api_response


@extend_schema_view(
    list=extend_schema(
        summary="List orders",
        description="List orders for the owner of that order",
        tags=["Orders"],
    ),
    retrieve=extend_schema(
        summary="Retrieve order",
        description="Get order details by id",
        tags=["Orders"],
    ),
    create=extend_schema(
        summary="Create order",
        description="Place a new order",
        tags=["Orders"],
    ),
    update=extend_schema(
        summary="Update order",
        description="Update an existing order "
        "only shipping address allowed to update",
        tags=["Orders"],
    ),
    partial_update=extend_schema(
        summary="Partial update order only shipping address allowed to change",
        tags=["Orders"],
    ),
    destroy=extend_schema(summary="Cancel order", tags=["Orders"]),
)
class OrderViewSet(viewsets.ModelViewSet):
    """Provides CRUD endpoints for orders owned by the authenticated
    user.

    All responses use the unified api_response structure and access is
    restricted to the order owner.
    """

    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOnly]

    def get_queryset(self):
        """Returns orders belonging to the current
        authenticated user.
        """
        log_debug(
            "Fetching orders for user",
            extra={"user_id": self.request.user.id},
        )
        return Order.objects.filter(user=self.request.user).order_by(
            "-order_date",
        )

    def create(self, request, *args, **kwargs):
        """Creates an order and return a wrapped API response."""
        response = super().create(request, *args, **kwargs)
        return api_response(
            True,
            message=SuccessMessages.ORDER_PLACED.value,
            data=response.data,
            status_code=response.status_code,
        )

    def perform_create(self, serializer):
        """Saves a new order, recompute total, and log creation
        details.
        """
        try:
            order = serializer.save()
            order.recompute_total()
            log_info(
                "Order created",
                extra={"order_id": order.id, "user_id": self.request.user.id},
            )
            return order
        except Exception as exc:
            log_error("Failed to create order", extra={"error": str(exc)})
            raise
