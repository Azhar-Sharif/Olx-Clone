import logging

from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions, status
from rest_framework.views import APIView

from core.utils.enums import ErrorMessages, SuccessMessages
from core.utils.logger import log_debug, log_error, log_info
from core.utils.response import api_response
from users.models import User
from users.serializers import (
    LoginSerializer,
    UserProfileUpdateSerializer,
    UserSerializer,
)

logger = logging.getLogger(__name__)


class UserCreateView(generics.CreateAPIView):
    """Register a new user"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    return api_response(
        True,
        message=SuccessMessages.USER_CREATED.value,
        data=response.data,
        status_code=response.status_code,
    )


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
    Authenticated user can view, update, or delete their own profile
    """

    serializer_class = UserProfileUpdateSerializer

    def get_object(self):
        return self.request.user


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        client_ip = request.META.get("REMOTE_ADDR", "Unknown")
        serializer = LoginSerializer(data=request.data)

        log_info(
            "Login attempt",
            extra={"ip": client_ip, "username": request.data.get("username")},
        )

        if not serializer.is_valid():
            log_error(
                f"Invalid login data from IP {client_ip}",
                extra={"errors": serializer.errors},
            )

            errors = serializer.errors
            username_blank = "username" in errors and any(
                "may not be blank" in str(msg) or "required" in str(msg)
                for msg in errors["username"]
            )
            password_blank = "password" in errors and any(
                "may not be blank" in str(msg) or "required" in str(msg)
                for msg in errors["password"]
            )

            if username_blank or password_blank:
                return api_response(
                    success=False,
                    message="Username and password field required",
                    data=None,
                    errors=errors,
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            return api_response(
                success=False,
                message="Validation error occurred.",
                data=None,
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        log_debug(f"Authenticating user {username}")

        user = authenticate(request, username=username, password=password)
        if user is None:
            log_warning_msg = f"Failed login attempt for '{username}' from IP {client_ip} - Invalid credentials"
            log_error(log_warning_msg)
            return api_response(
                success=False,
                message=ErrorMessages.INVALID_CREDENTIALS.value,
                data=None,
                errors={"detail": "Invalid username or password."},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user)
        user_data = UserSerializer(user).data
        log_info("User logged in", extra={"user_id": user.id})
        return api_response(
            success=True,
            message=SuccessMessages.USER_LOGGED_IN.value,
            data=user_data,
            status_code=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return api_response(
            True, message=SuccessMessages.USER_LOGGED_OUT.value, data=None
        )
