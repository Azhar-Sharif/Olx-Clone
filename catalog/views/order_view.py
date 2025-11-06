from rest_framework import permissions, viewsets

from catalog.models import Order

from .permissions import IsOwnerOnly
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOnly]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by(
            "-order_date"
        )

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        order.recompute_total()
        return order
