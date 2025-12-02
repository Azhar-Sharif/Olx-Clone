from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)

from catalog.serializers.product import ProductSerializer
from docs.catalog.utils.examples_products import (
    product_auth_required_example,
    product_create_request_example,
    product_create_success_example,
    product_detail_success_example,
    product_list_empty_success_example,
    product_list_success_example,
    product_not_found_example,
    product_partial_update_request_example,
    product_permission_denied_example,
    product_server_error_example,
    product_update_request_example,
    product_validation_error_example,
)

product_list_schema = extend_schema(
    summary="List products",
    description="Retrieve a list of products.",
    responses={
        200: OpenApiResponse(
            description="Products retrieved successfully.",
            examples=[
                OpenApiExample(
                    "Product List",
                    value=product_list_success_example,
                ),
                OpenApiExample(
                    "Empty Product List",
                    value=product_list_empty_success_example,
                ),
            ],
        ),
        401: OpenApiResponse(
            description="Authentication required.",
            examples=[
                OpenApiExample(
                    "Not authenticated",
                    value=product_auth_required_example,
                ),
            ],
        ),
        500: OpenApiResponse(
            description="Internal server error.",
            examples=[
                OpenApiExample(
                    "Server error",
                    value=product_server_error_example,
                ),
            ],
        ),
    },
    tags=["Products"],
)

product_retrieve_schema = extend_schema(
    summary="Retrieve product",
    description="Get product details by ID.",
    responses={
        200: OpenApiResponse(
            description="Product retrieved successfully.",
            examples=[
                OpenApiExample(
                    "Product Detail",
                    value=product_detail_success_example,
                ),
            ],
        ),
        401: OpenApiResponse(
            description="Authentication required.",
            examples=[
                OpenApiExample(
                    "Not authenticated",
                    value=product_auth_required_example,
                ),
            ],
        ),
        404: OpenApiResponse(
            description="Product not found.",
            examples=[
                OpenApiExample(
                    "Product Not Found",
                    value=product_not_found_example,
                ),
            ],
        ),
        500: OpenApiResponse(
            description="Internal server error.",
            examples=[
                OpenApiExample(
                    "Server error",
                    value=product_server_error_example,
                ),
            ],
        ),
    },
    tags=["Products"],
)

product_create_schema = extend_schema(
    summary="Create product",
    description="Create a new product.",
    request=ProductSerializer,
    responses={
        201: OpenApiResponse(
            description="Product created successfully.",
            examples=[
                OpenApiExample(
                    "Product Created",
                    value=product_create_success_example,
                ),
            ],
        ),
        400: OpenApiResponse(
            description="Validation error.",
            examples=[
                OpenApiExample(
                    "Validation Error",
                    value=product_validation_error_example,
                ),
            ],
        ),
        401: OpenApiResponse(
            description="Authentication required.",
            examples=[
                OpenApiExample(
                    "Not authenticated",
                    value=product_auth_required_example,
                ),
            ],
        ),
        403: OpenApiResponse(
            description="Permission denied.",
            examples=[
                OpenApiExample(
                    "Forbidden",
                    value=product_permission_denied_example,
                ),
            ],
        ),
        500: OpenApiResponse(
            description="Internal server error.",
            examples=[
                OpenApiExample(
                    "Server error",
                    value=product_server_error_example,
                ),
            ],
        ),
    },
    examples=[
        OpenApiExample(
            "Create Product Request",
            value=product_create_request_example,
        ),
    ],
    tags=["Products"],
)


product_update_schema = extend_schema(
    summary="Update product",
    description="Update an existing product.",
    request=ProductSerializer,
    responses={
        200: OpenApiResponse(
            description="Product updated successfully.",
            examples=[
                OpenApiExample(
                    "Product Updated",
                    value=product_create_success_example,
                ),
            ],
        ),
        400: OpenApiResponse(
            description="Validation error.",
            examples=[
                OpenApiExample(
                    "Validation Error",
                    value=product_validation_error_example,
                ),
            ],
        ),
        401: OpenApiResponse(
            description="Authentication required.",
            examples=[
                OpenApiExample(
                    "Not authenticated",
                    value=product_auth_required_example,
                ),
            ],
        ),
        403: OpenApiResponse(
            description="Permission denied.",
            examples=[
                OpenApiExample(
                    "Forbidden",
                    value=product_permission_denied_example,
                ),
            ],
        ),
        404: OpenApiResponse(
            description="Product not found.",
            examples=[
                OpenApiExample(
                    "Product Not Found",
                    value=product_not_found_example,
                ),
            ],
        ),
        500: OpenApiResponse(
            description="Internal server error.",
            examples=[
                OpenApiExample(
                    "Server error",
                    value=product_server_error_example,
                ),
            ],
        ),
    },
    examples=[
        OpenApiExample(
            "Update Product Request",
            value=product_update_request_example,
        ),
    ],
    tags=["Products"],
)

product_partial_update_schema = extend_schema(
    summary="Partial update product",
    description="Partially update an existing product.",
    request=ProductSerializer,
    responses={
        200: OpenApiResponse(
            description="Product updated successfully.",
            examples=[
                OpenApiExample(
                    "Product Updated",
                    value=product_create_success_example,
                ),
            ],
        ),
        400: OpenApiResponse(
            description="Validation error.",
            examples=[
                OpenApiExample(
                    "Validation Error",
                    value=product_validation_error_example,
                ),
            ],
        ),
        401: OpenApiResponse(
            description="Authentication required.",
            examples=[
                OpenApiExample(
                    "Not authenticated",
                    value=product_auth_required_example,
                ),
            ],
        ),
        403: OpenApiResponse(
            description="Permission denied.",
            examples=[
                OpenApiExample(
                    "Forbidden",
                    value=product_permission_denied_example,
                ),
            ],
        ),
        404: OpenApiResponse(
            description="Product not found.",
            examples=[
                OpenApiExample(
                    "Product Not Found",
                    value=product_not_found_example,
                ),
            ],
        ),
        500: OpenApiResponse(
            description="Internal server error.",
            examples=[
                OpenApiExample(
                    "Server error",
                    value=product_server_error_example,
                ),
            ],
        ),
    },
    examples=[
        OpenApiExample(
            "Partial Update Product Request",
            value=product_partial_update_request_example,
        ),
    ],
    tags=["Products"],
)


product_destroy_schema = extend_schema(
    summary="Delete product",
    description="Delete an existing product.",
    responses={
        200: OpenApiResponse(
            description="Product deleted successfully.",
            examples=[
                OpenApiExample(
                    "Product Deleted",
                    value={
                        "success": True,
                        "message": "Product deleted successfully.",
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
                    value=product_auth_required_example,
                ),
            ],
        ),
        403: OpenApiResponse(
            description="Permission denied.",
            examples=[
                OpenApiExample(
                    "Forbidden",
                    value=product_permission_denied_example,
                ),
            ],
        ),
        404: OpenApiResponse(
            description="Product not found.",
            examples=[
                OpenApiExample(
                    "Product Not Found",
                    value=product_not_found_example,
                ),
            ],
        ),
        500: OpenApiResponse(
            description="Internal server error.",
            examples=[
                OpenApiExample(
                    "Server error",
                    value=product_server_error_example,
                ),
            ],
        ),
    },
    tags=["Products"],
)
