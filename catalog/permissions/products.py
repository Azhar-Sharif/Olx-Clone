from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow read-only access for all users;
    write access only for owners.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
