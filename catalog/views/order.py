"""Order API views.

Exposes endpoints for listing, retrieving, creating, updating, and
canceling orders for the authenticated owner using the api_response
wrapper.
"""

from drf_spectacular.utils import extend_schema_view
from rest_framework import permissions, viewsets

from catalog.models import Order
from catalog.permissions import IsOwnerOnly
from catalog.serializers import OrderSerializer
from core.utils.enums import SuccessMessages
from core.utils.logger import log_debug, log_error, log_info
from core.utils.response import api_response
from docs.catalog.docs_orders import (
    order_create_schema,
    order_destroy_schema,
    order_list_schema,
    order_partial_update_schema,
    order_retrieve_schema,
    order_update_schema,
)


@extend_schema_view(
    list=order_list_schema,
    retrieve=order_retrieve_schema,
    create=order_create_schema,
    update=order_update_schema,
    partial_update=order_partial_update_schema,
    destroy=order_destroy_schema,
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
