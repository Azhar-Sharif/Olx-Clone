from rest_framework import generics, permissions

from user.models import User
from user.serializers.serializers_user import UserSerializer


class UserCreateView(generics.CreateAPIView):
    """Register a new user"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data.get("password"))
        user.save()


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
    Authenticated user can view, update, or delete their own profile
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
