"""Order API views.

Exposes endpoints for listing, retrieving, creating, updating, and
canceling orders for the authenticated owner using the api_response
wrapper.
"""

from drf_spectacular.utils import extend_schema_view
from rest_framework import permissions, status, viewsets

from catalog.models import Order
from catalog.permissions import IsOwnerOnly
from catalog.serializers import OrderSerializer
from core.utils.enums import SuccessMessages
from core.utils.logger import log_debug, log_info
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

    def list(self, request, *args, **kwargs):  # noqa: A003
        """List orders and wrap response in api_response."""
        log_info("Order list called", extra={"user_id": request.user.id})
        response = super().list(request, *args, **kwargs)
        return api_response(
            True,
            message=SuccessMessages.ORDERS_LISTED.value,
            data=response.data,
            status_code=response.status_code,
        )

    def retrieve(self, request, *args, **kwargs):
        """Retrieve order details and wrap response in api_response."""
        log_info("Order retrieve called", extra={"user_id": request.user.id})
        response = super().retrieve(request, *args, **kwargs)
        return api_response(
            True,
            message=SuccessMessages.ORDER_RETRIEVED.value,
            data=response.data,
            status_code=response.status_code,
        )

    def create(self, request, *args, **kwargs):
        """Creates an order and return a wrapped API response."""
        log_info("Order create called", extra={"user_id": request.user.id})
        log_debug(
            "Order create payload",
            extra={"data": request.data},
        )
        response = super().create(request, *args, **kwargs)
        return api_response(
            True,
            message=SuccessMessages.ORDER_PLACED.value,
            data=response.data,
            status_code=response.status_code,
        )

    def update(self, request, *args, **kwargs):
        """Update an order's shipping address and wrap response."""
        log_info("Order update called", extra={"user_id": request.user.id})
        response = super().update(request, *args, **kwargs)
        log_info(
            "Order updated",
            extra={
                "order_id": response.data.get("id"),
                "user_id": request.user.id,
            },
        )
        return api_response(
            True,
            message=SuccessMessages.ORDER_UPDATED.value,
            data=response.data,
            status_code=response.status_code,
        )

    def destroy(self, request, *args, **kwargs):
        """Cancel (delete) an order and wrap response."""
        order = self.get_object()
        order_id = order.id
        user_id = request.user.id
        log_info(
            "Order delete called",
            extra={"order_id": order_id, "user_id": user_id},
        )

        super().destroy(request, *args, **kwargs)

        log_info(
            "Order deleted",
            extra={"order_id": order_id, "user_id": user_id},
        )
        return api_response(
            True,
            message=SuccessMessages.ORDER_CANCELLED.value,
            data=None,
            status_code=status.HTTP_200_OK,
        )
