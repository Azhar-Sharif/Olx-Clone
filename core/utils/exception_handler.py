# core/utils/exception_handler.py
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from core.utils.enums import ErrorMessages
from core.utils.response import api_response


def handle_validation_error(detail):
    """Handle all validation-related errors."""
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


def handle_api_exception(exc, response):
    detail = (
        response.data
        if response is not None
        else getattr(exc, "detail", str(exc))
    )
    code = getattr(exc, "status_code", status.HTTP_400_BAD_REQUEST)
    return Response(
        {
            "success": False,
            "message": ErrorMessages.SERVER_ERROR.value,
            "data": None,
            "errors": detail,
        },
        status=code,
    )


def handle_exceptions(exc, context):
    response = drf_exception_handler(exc, context)

    if isinstance(exc, exceptions.ValidationError):
        return handle_validation_error(
            response.data if response else getattr(exc, "detail", str(exc))
        )
    if isinstance(exc, Http404):
        return handle_404(exc, context)
    if isinstance(exc, exceptions.PermissionDenied):
        return api_response(
            False,
            ErrorMessages.PERMISSION_DENIED.value,
            data=None,
            errors={"detail": str(exc)},
        )
    if isinstance(exc, exceptions.APIException):
        return handle_api_exception(exc, response)
    if response is None:
        return api_response(
            False,
            ErrorMessages.SERVER_ERROR.value,
            data=None,
            errors={"detail": "Server error."},
        )

    return api_response(
        False,
        ErrorMessages.SERVER_ERROR.value,
        data=None,
        errors=response.data,
    )
