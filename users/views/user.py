import logging

from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import LoginSerializer, UserSerializer

logger = logging.getLogger(__name__)


class UserCreateView(generics.CreateAPIView):
    """Register a new user"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
    Authenticated user can view, update, or delete their own profile
    """

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        client_ip = request.META.get("REMOTE_ADDR", "Unknown")
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                user_serializer = UserSerializer(user)
                return Response(
                    {
                        "message": "Login successful",
                        "user": user_serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            logger.warning(
                f"Failed login attempt: {username} from IP: {client_ip} - Invalid credentials"
            )
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        logger.warning(
            f"Invalid login data from IP: {client_ip} - {serializer.errors}"
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )
