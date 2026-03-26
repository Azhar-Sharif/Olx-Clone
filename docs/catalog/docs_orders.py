from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)

from catalog.serializers import OrderSerializer
from docs.catalog.utils.examples_orders import (
    order_auth_required_example,
    order_create_request_example,
    order_create_success_example,
    order_detail_success_example,
    order_inventory_error_example,
    order_list_empty_success_example,
    order_list_success_example,
    order_not_found_example,
    order_partial_update_request_example,
    order_partial_update_success_example,
    order_permission_denied_example,
    order_server_error_example,
    order_update_request_example,
    order_update_success_example,
    order_validation_error_example,
)

order_list_schema = extend_schema(
    summary="List orders",
    description="List orders for the authenticated owner.",
    responses={
        200: OpenApiResponse(
            description="Orders listed successfully.",
            examples=[
                OpenApiExample("Order List", value=order_list_success_example),
                OpenApiExample(
                    "Empty Order List",
                    value=order_list_empty_success_example,
                ),
            ],
        ),
        401: OpenApiResponse(
            description="Authentication required.",
            examples=[
                OpenApiExample(
                    "Not authenticated",
                    value=order_auth_required_example,
                ),
            ],
        ),
        500: OpenApiResponse(
            description="Internal server error.",
            examples=[
                OpenApiExample(
                    "Server error",
                    value=order_server_error_example,
                ),
            ],
        ),
    },
    tags=["Orders"],
)

order_retrieve_schema = extend_schema(
    summary="Retrieve order",
    description="Get order details by ID for the authenticated owner.",
    responses={
        200: OpenApiResponse(
            description="Order retrieved successfully.",
            examples=[
                OpenApiExample(
                    "Order Detail",
                    value=order_detail_success_example,
                ),
            ],
        ),
        401: OpenApiResponse(
            description="Authentication required.",
            examples=[
                OpenApiExample(
                    "Not authenticated",
                    value=order_auth_required_example,
                ),
            ],
        ),
        403: OpenApiResponse(
            description="Permission denied.",
            examples=[
                OpenApiExample(
                    "Forbidden",
                    value=order_permission_denied_example,
                ),
            ],
        ),
        404: OpenApiResponse(
            description="Order not found.",
            examples=[
                OpenApiExample(
                    "Order Not Found",
                    value=order_not_found_example,
                ),
            ],
        ),
        500: OpenApiResponse(
            description="Internal server error.",
            examples=[
                OpenApiExample(
                    "Server error",
                    value=order_server_error_example,
                ),
            ],
        ),
    },
    tags=["Orders"],
)

order_create_schema = extend_schema(
    summary="Create order",
    description="Place a new order for the authenticated user.",
    request=OrderSerializer,
    responses={
        201: OpenApiResponse(
            description="Order placed successfully.",
            examples=[
                OpenApiExample(
                    "Order Created",
                    value=order_create_success_example,
                ),
            ],
        ),
        400: OpenApiResponse(
            description="Validation error.",
            examples=[
                OpenApiExample(
                    "Inventory Not Available",
                    value=order_inventory_error_example,
                ),
                OpenApiExample(
                    "Validation Error",
                    value=order_validation_error_example,
                ),
            ],
        ),
        401: OpenApiResponse(
            description="Authentication required.",
            examples=[
                OpenApiExample(
                    "Not authenticated",
                    value=order_auth_required_example,
                ),
            ],
        ),
        500: OpenApiResponse(
            description="Internal server error.",
            examples=[
                OpenApiExample(
                    "Server error",
                    value=order_server_error_example,
                ),
            ],
        ),
    },
    examples=[
        OpenApiExample(
            "Create Order Request",
            value=order_create_request_example,
        ),
    ],
    tags=["Orders"],
)

order_update_schema = extend_schema(
    summary="Update order",
    description="Update an existing order (only shipping address allowed).",
    request=OrderSerializer,
    responses={
        200: OpenApiResponse(
            description="Order updated successfully.",
            examples=[
                OpenApiExample(
                    "Order Updated",
                    value=order_detail_success_example,
                ),
            ],
        ),
        400: OpenApiResponse(
            description="Validation error.",
            examples=[
                OpenApiExample(
                    "Validation Error",
                    value=order_validation_error_example,
                ),
            ],
        ),
        401: OpenApiResponse(
            description="Authentication required.",
            examples=[
                OpenApiExample(
                    "Not authenticated",
                    value=order_auth_required_example,
                ),
            ],
        ),
        403: OpenApiResponse(
            description="Permission denied.",
            examples=[
                OpenApiExample(
                    "Forbidden",
                    value=order_permission_denied_example,
                ),
            ],
        ),
        404: OpenApiResponse(
            description="Order not found.",
            examples=[
                OpenApiExample(
                    "Order Not Found",
                    value=order_not_found_example,
                ),
            ],
        ),
        500: OpenApiResponse(
            description="Internal server error.",
            examples=[
                OpenApiExample(
                    "Server error",
                    value=order_server_error_example,
                ),
            ],
        ),
    },
    tags=["Orders"],
)

order_partial_update_schema = extend_schema(
    summary="Partial update order",
    description=(
        "Partially update an existing order "
        "           only shipping address allowed)."
    ),
    request=OrderSerializer,
    responses={
        200: OpenApiResponse(
            description="Order updated successfully.",
            examples=[
                OpenApiExample(
                    "Order Updated",
                    value=order_detail_success_example,
                ),
            ],
        ),
        400: OpenApiResponse(
            description="Validation error.",
            examples=[
                OpenApiExample(
                    "Validation Error",
                    value=order_validation_error_example,
                ),
            ],
        ),
        401: OpenApiResponse(
            description="Authentication required.",
            examples=[
                OpenApiExample(
                    "Not authenticated",
                    value=order_auth_required_example,
                ),
            ],
        ),
        403: OpenApiResponse(
            description="Permission denied.",
            examples=[
                OpenApiExample(
                    "Forbidden",
                    value=order_permission_denied_example,
                ),
            ],
        ),
        404: OpenApiResponse(
            description="Order not found.",
            examples=[
                OpenApiExample(
                    "Order Not Found",
                    value=order_not_found_example,
                ),
            ],
        ),
        500: OpenApiResponse(
            description="Internal server error.",
            examples=[
                OpenApiExample(
                    "Server error",
                    value=order_server_error_example,
                ),
            ],
        ),
    },
    tags=["Orders"],
)

order_destroy_schema = extend_schema(
    summary="Cancel order",
    description="Cancel an existing order.",
    responses={
        200: OpenApiResponse(
            description="Order cancelled successfully.",
            examples=[
                OpenApiExample(
                    "Order Cancelled",
                    value={
                        "success": True,
                        "message": "Order cancelled successfully.",
                        "data": None,
                        "errors": None,
                    },
                ),
            ],
        ),
        401: OpenApiResponse(
            description="Authentication required.",
            examples=[
                OpenApiExample(
                    "Not authenticated",
                    value=order_auth_required_example,
                ),
            ],
        ),
        403: OpenApiResponse(
            description="Permission denied.",
            examples=[
                OpenApiExample(
                    "Forbidden",
                    value=order_permission_denied_example,
                ),
            ],
        ),
        404: OpenApiResponse(
            description="Order not found.",
            examples=[
                OpenApiExample(
                    "Order Not Found",
                    value=order_not_found_example,
                ),
            ],
        ),
        500: OpenApiResponse(
            description="Internal server error.",
            examples=[
                OpenApiExample(
                    "Server error",
                    value=order_server_error_example,
                ),
            ],
        ),
    },
    tags=["Orders"],
)


order_update_schema = extend_schema(
    summary="Update order",
    description="Update an existing order (only shipping address allowed).",
    request=OrderSerializer,
    responses={
        200: OpenApiResponse(
            description="Order updated successfully.",
            examples=[
                OpenApiExample(
                    "Order Updated",
                    value=order_update_success_example,
                ),
            ],
        ),
        400: OpenApiResponse(
            description="Validation error.",
            examples=[
                OpenApiExample(
                    "Validation Error",
                    value=order_validation_error_example,
                ),
            ],
        ),
        401: OpenApiResponse(
            description="Authentication required.",
            examples=[
                OpenApiExample(
                    "Not authenticated",
                    value=order_auth_required_example,
                ),
            ],
        ),
        403: OpenApiResponse(
            description="Permission denied.",
            examples=[
                OpenApiExample(
                    "Forbidden",
                    value=order_permission_denied_example,
                ),
            ],
        ),
        404: OpenApiResponse(
            description="Order not found.",
            examples=[
                OpenApiExample(
                    "Order Not Found",
                    value=order_not_found_example,
                ),
            ],
        ),
        500: OpenApiResponse(
            description="Internal server error.",
            examples=[
                OpenApiExample(
                    "Server error",
                    value=order_server_error_example,
                ),
            ],
        ),
    },
    examples=[
        OpenApiExample(
            "Update Order Request",
            value=order_update_request_example,
        ),
    ],
    tags=["Orders"],
)

order_partial_update_schema = extend_schema(
    summary="Partial update order",
    description=(
        "Partially update an existing order " "only shipping address allowed)."
    ),
    request=OrderSerializer,
    responses={
        200: OpenApiResponse(
            description="Order updated successfully.",
            examples=[
                OpenApiExample(
                    "Order Partially Updated",
                    value=order_partial_update_success_example,
                ),
            ],
        ),
        400: OpenApiResponse(
            description="Validation error.",
            examples=[
                OpenApiExample(
                    "Validation Error",
                    value=order_validation_error_example,
                ),
            ],
        ),
        401: OpenApiResponse(
            description="Authentication required.",
            examples=[
                OpenApiExample(
                    "Not authenticated",
                    value=order_auth_required_example,
                ),
            ],
        ),
        403: OpenApiResponse(
            description="Permission denied.",
            examples=[
                OpenApiExample(
                    "Forbidden",
                    value=order_permission_denied_example,
                ),
            ],
        ),
        404: OpenApiResponse(
            description="Order not found.",
            examples=[
                OpenApiExample(
                    "Order Not Found",
                    value=order_not_found_example,
                ),
            ],
        ),
        500: OpenApiResponse(
            description="Internal server error.",
            examples=[
                OpenApiExample(
                    "Server error",
                    value=order_server_error_example,
                ),
            ],
        ),
    },
    examples=[
        OpenApiExample(
            "Partial Update Order Request",
            value=order_partial_update_request_example,
        ),
    ],
    tags=["Orders"],
)
