from rest_framework import permissions, viewsets

from catalog.models import Order
from catalog.permissions import IsOwnerOnly
from catalog.serializers import OrderSerializer
from core.utils.enums import SuccessMessages
from core.utils.logger import log_debug, log_error, log_info
from core.utils.response import api_response


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOnly]

    def get_queryset(self):
        log_debug(
            "Fetching orders for user", extra={"user_id": self.request.user.id}
        )
        return Order.objects.filter(user=self.request.user).order_by(
            "-order_date"
        )

    def create(self, request, *args, **kwargs):
        """Override create to return unified response structure."""
        response = super().create(request, *args, **kwargs)
        return api_response(
            True,
            message=SuccessMessages.ORDER_PLACED.value,
            data=response.data,
            status_code=response.status_code,
        )

    def perform_create(self, serializer):
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
