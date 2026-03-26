from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.views import exception_handler as drf_exception_handler

from core.utils.enums import ErrorMessages
from core.utils.response import api_response

from .logger import log_error


def handle_validation_error(detail, request=None):  # noqa: C901
    """Handle all validation-related errors and log them."""
    if request:
        user = getattr(request, "user", None)
        log_error(
            f"ValidationError: {detail}",
            extra={
                "path": getattr(request, "path", None),
                "method": getattr(request, "method", None),
                "user_id": getattr(user, "id", None),
            },
        )

    detail_str = str(detail)

    if "Inventory check failed" in detail_str:
        return api_response(
            False,
            ErrorMessages.INVENTORY_NOT_AVAILABLE.value,
            data=None,
            errors=detail,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if "Price must be zero or positive" in detail_str:
        return api_response(
            False,
            ErrorMessages.VALIDATION_ERROR.value,
            data=None,
            errors=detail,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if "Username and password are required" in detail_str:
        return api_response(
            False,
            ErrorMessages.INVALID_CREDENTIALS.value,
            data=None,
            errors=detail,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if "already exists" in detail_str:
        return api_response(
            False,
            ErrorMessages.USERNAME_TAKEN.value,
            data=None,
            errors=detail,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    missing_fields = []
    if isinstance(detail, dict):
        for field, errors_list in detail.items():
            if not isinstance(errors_list, (list, tuple)):
                errors_list = [errors_list]
            for e in errors_list:
                e_str = str(e)
                if (
                    "may not be blank" in e_str
                    or "This field is required" in e_str
                ):
                    missing_fields.append(field)

    if missing_fields:
        return api_response(
            False,
            "The following fields are required",
            data=None,
            errors=detail,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return api_response(
        False,
        ErrorMessages.VALIDATION_ERROR.value,
        data=None,
        errors=detail,
        status_code=status.HTTP_400_BAD_REQUEST,
    )


def handle_404(exc, context):
    """Handle Http404 with logging."""
    request = context.get("request")
    if request:
        user = getattr(request, "user", None)
        log_error(
            f"Http404: {str(exc)}",
            extra={
                "path": getattr(request, "path", None),
                "method": getattr(request, "method", None),
                "user_id": getattr(user, "id", None),
            },
        )

    view = context.get("view", None)
    if view:
        model = getattr(getattr(view, "queryset", None), "model", None)
        if model:
            model_name = model.__name__
            mapping = {
                "Order": ErrorMessages.ORDER_NOT_FOUND.value,
                "Product": ErrorMessages.PRODUCT_NOT_FOUND.value,
                "Category": ErrorMessages.CATEGORY_NOT_FOUND.value,
                "User": ErrorMessages.USER_NOT_FOUND.value,
            }
            return api_response(
                False,
                mapping.get(model_name, ErrorMessages.NOT_FOUND.value),
                data=None,
                errors={"detail": "Not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

    return api_response(
        False,
        ErrorMessages.NOT_FOUND.value,
        data=None,
        errors={"detail": "Not found."},
        status_code=status.HTTP_404_NOT_FOUND,
    )


def handle_permission_error(exc, request=None):
    """Handle 403 / CSRF-like permission errors with logging."""
    if request:
        user = getattr(request, "user", None)
        log_error(
            f"PermissionDenied/CSRF: {str(exc)}",
            extra={
                "path": getattr(request, "path", None),
                "method": getattr(request, "method", None),
                "user_id": getattr(user, "id", None),
            },
        )

    return api_response(
        False,
        ErrorMessages.PERMISSION_DENIED.value,
        data=None,
        errors={"detail": str(exc)},
        status_code=status.HTTP_403_FORBIDDEN,
    )


def handle_api_exception(exc, response, request=None):
    """Handle generic DRF APIException with logging."""
    detail = response.data if response else getattr(exc, "detail", str(exc))
    code = getattr(exc, "status_code", status.HTTP_400_BAD_REQUEST)

    if request:
        user = getattr(request, "user", None)
        log_error(
            f"APIException: {detail}",
            extra={
                "path": getattr(request, "path", None),
                "method": getattr(request, "method", None),
                "user_id": getattr(user, "id", None),
                "status_code": code,
            },
        )

    if isinstance(
        exc,
        (exceptions.NotAuthenticated, exceptions.AuthenticationFailed),
    ):
        return api_response(
            False,
            ErrorMessages.AUTH_REQUIRED.value,
            data=None,
            errors=detail,
            status_code=code,
        )

    return api_response(
        False,
        ErrorMessages.SERVER_ERROR.value,
        data=None,
        errors=detail,
        status_code=code,
    )


def handle_exceptions(exc, context):
    """Main custom exception handler with logging."""
    response = drf_exception_handler(exc, context)
    request = context.get("request")

    if isinstance(exc, exceptions.ValidationError):
        detail = (
            response.data if response else getattr(exc, "detail", str(exc))
        )
        return handle_validation_error(detail, request=request)

    if isinstance(exc, Http404):
        return handle_404(exc, context)

    if isinstance(exc, (exceptions.PermissionDenied, DjangoPermissionDenied)):
        return handle_permission_error(exc, request=request)

    if isinstance(exc, exceptions.APIException):
        return handle_api_exception(exc, response, request=request)

    if response is None:
        if request:
            user = getattr(request, "user", None)
            log_error(
                f"Unhandled exception: {str(exc)}",
                extra={
                    "path": getattr(request, "path", None),
                    "method": getattr(request, "method", None),
                    "user_id": getattr(user, "id", None),
                },
            )
        return api_response(
            False,
            ErrorMessages.SERVER_ERROR.value,
            data=None,
            errors={"detail": "Server error."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if request:
        user = getattr(request, "user", None)
        log_error(
            f"Exception handled by DRF: {response.data}",
            extra={
                "path": getattr(request, "path", None),
                "method": getattr(request, "method", None),
                "user_id": getattr(user, "id", None),
            },
        )

    return api_response(
        False,
        ErrorMessages.SERVER_ERROR.value,
        data=None,
        errors=response.data,
        status_code=getattr(
            response,
            "status_code",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        ),
    )
