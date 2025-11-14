# core/utils/exception_handler.py
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.response import Response
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

    if "Inventory check failed" in str(detail):
        return api_response(
            False,
            ErrorMessages.INVENTORY_NOT_AVAILABLE.value,
            data=None,
            errors=detail,
        )
    if "Price must be zero or positive" in str(detail):
        return api_response(
            False,
            ErrorMessages.VALIDATION_ERROR.value,
            data=None,
            errors=detail,
        )
    if "Username and password are required" in str(detail):
        return api_response(
            False,
            ErrorMessages.INVALID_CREDENTIALS.value,
            data=None,
            errors=detail,
        )
    if "already exists" in str(detail):
        return api_response(
            False, ErrorMessages.USERNAME_TAKEN.value, data=None, errors=detail
        )
    missing_fields = []
    if isinstance(detail, dict):
        for field, errors_list in detail.items():
            for e in errors_list:
                if "may not be blank" in str(
                    e
                ) or "This field is required" in str(e):
                    missing_fields.append(field)
    if missing_fields:
        return api_response(
            False,
            "The following fields are required",
            data=None,
            errors=detail,
        )

    return api_response(
        False, ErrorMessages.VALIDATION_ERROR.value, data=None, errors=detail
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
        model_name = getattr(getattr(view, "queryset", None), "model", None)
        if model_name:
            model_name = model_name.__name__
            mapping = {
                "Order": ErrorMessages.ORDER_NOT_FOUND.value,
                "Product": ErrorMessages.PRODUCT_NOT_FOUND.value,
                "Category": ErrorMessages.CATEGORY_NOT_FOUND.value,
                "User": ErrorMessages.USER_NOT_FOUND.value,
            }
            return api_response(
                False,
                mapping.get(model_name, ErrorMessages.SERVER_ERROR.value),
                data=None,
                errors={"detail": "Not found."},
            )

    return api_response(
        False,
        ErrorMessages.SERVER_ERROR.value,
        data=None,
        errors={"detail": "Not found."},
    )


def handle_api_exception(exc, response, request=None):
    """Handle DRF APIException with logging."""
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

    payload = {
        "success": False,
        "message": ErrorMessages.SERVER_ERROR.value,
        "data": None,
        "errors": detail,
    }
    return Response(payload, status=code)


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

    if isinstance(exc, exceptions.PermissionDenied):
        if request:
            user = getattr(request, "user", None)
            log_error(
                f"PermissionDenied: {str(exc)}",
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
        )

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
    )
