from rest_framework import permissions


class IsOwnerOnly(permissions.BasePermission):
    """
    Allow only the order owner to view or modify their own orders.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
