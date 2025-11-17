import logging

from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied, ValidationError
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


@extend_schema_view(
    post=extend_schema(
        summary="Register user",
        description="Create a new user account",
        tags=["Users"],
    )
)
class UserCreateView(generics.CreateAPIView):
    """Register a new user.

    Request body (example):
    {
      "username": "johndoe",
      "email": "john@example.com",
      "password": "secret123",
      "first_name": "John",
      "last_name": "Doe"
    }

    Success response (api_response wrapper) example:
    {
      "success": true,
      "message": "User created successfully.",
      "data": { ...user fields... },
      "errors": null
    }
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        log_debug(
            "User registration payload",
            extra={
                "data": {
                    k: v
                    for k, v in request.data.items()
                    if k.lower() not in ("password",)
                }
            },
        )
        response = super().create(request, *args, **kwargs)
        log_info("User created", extra={"user_id": response.data.get("id")})
        return api_response(
            True,
            message=SuccessMessages.USER_CREATED.value,
            data=response.data,
            status_code=response.status_code,
        )


@extend_schema_view(
    get=extend_schema(
        summary="Get profile",
        description="Retrieve the authenticated user's profile",
        tags=["Users"],
    ),
    put=extend_schema(
        summary="Update profile",
        description="Update the authenticated user's profile",
        tags=["Users"],
    ),
    patch=extend_schema(summary="Partial update profile", tags=["Users"]),
    delete=extend_schema(summary="Delete account", tags=["Users"]),
)
class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
    Authenticated user can view, update, or delete their own profile.

    Responses are wrapped in the `api_response` structure.
    """

    serializer_class = UserProfileUpdateSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        """Full update (PUT) for the authenticated user's profile."""
        try:
            response = super().update(request, *args, **kwargs)
            log_info("Profile updated", extra={"user_id": request.user.id})
            return api_response(
                True,
                message="Profile updated",
                data=response.data,
                status_code=response.status_code,
            )

        except ValidationError as exc:
            log_error(
                "Profile update validation failed",
                extra={"error": exc.detail, "user_id": request.user.id},
            )
            return api_response(
                False,
                message="Validation failed",
                data=None,
                errors=exc.detail,
                status_code=400,
            )

        except PermissionDenied as exc:
            log_error(
                "Profile update permission denied",
                extra={"error": str(exc), "user_id": request.user.id},
            )
            return api_response(
                False,
                message="Permission denied",
                data=None,
                errors={"detail": str(exc)},
                status_code=403,
            )

        except Http404 as exc:
            log_error(
                "Profile update not found",
                extra={"error": str(exc), "user_id": request.user.id},
            )
            return api_response(
                False,
                message="User not found",
                data=None,
                errors={"detail": str(exc)},
                status_code=404,
            )

    def destroy(self, request, *args, **kwargs):
        """Delete the authenticated user's profile."""
        try:
            user_id = request.user.id
            super().destroy(request, *args, **kwargs)
            log_info("User deleted", extra={"user_id": user_id})
            return api_response(True, message="Profile deleted", data=None)

        except PermissionDenied as exc:
            log_error(
                "Profile deletion permission denied",
                extra={"error": str(exc), "user_id": request.user.id},
            )
            return api_response(
                False,
                message="Permission denied",
                data=None,
                errors={"detail": str(exc)},
                status_code=403,
            )

        except Http404 as exc:
            log_error(
                "Profile deletion not found",
                extra={"error": str(exc), "user_id": request.user.id},
            )
            return api_response(
                False,
                message="User not found",
                data=None,
                errors={"detail": str(exc)},
                status_code=404,
            )


class LoginView(APIView):
    """Login endpoint

    Request example:
    {
      "username": "johndoe",
      "password": "secret123"
    }

    Success response example:
    {
      "success": true,
      "message": "User logged in successfully.",
      "data": {"id": 1, "username": "johndoe"},
      "errors": null
    }
    """

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


@extend_schema_view(
    post=extend_schema(
        summary="Logout user",
        description="Logout the authenticated user",
        tags=["Users"],
    )
)
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        log_info("User logged out", extra={"user_id": request.user.id})
        return api_response(
            True, message=SuccessMessages.USER_LOGGED_OUT.value, data=None
        )
