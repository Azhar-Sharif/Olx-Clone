from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)

from docs.catalog.utils.examples_category import (
    category_detail_success_example,
    category_list_empty_success_example,
    category_list_success_example,
    category_server_error_example,
)

category_list_schema = extend_schema(
    summary="List categories",
    description="Retrieve a list of all categories.",
    responses={
        200: OpenApiResponse(
            description="Categories listed successfully.",
            examples=[
                OpenApiExample(
                    "Category List Success",
                    value=category_list_success_example,
                ),
                OpenApiExample(
                    "Empty Category List",
                    value=category_list_empty_success_example,
                ),
            ],
        ),
        500: OpenApiResponse(
            description="Internal server error.",
            examples=[
                OpenApiExample(
                    "Server error",
                    value=category_server_error_example,
                ),
            ],
        ),
    },
    tags=["Categories"],
)


category_detail_schema = extend_schema(
    summary="Retrieve category",
    description="Retrieve a single category by its ID.",
    responses={
        200: OpenApiResponse(
            description="Category retrieved successfully.",
            examples=[
                OpenApiExample(
                    "Category Detail Success",
                    value=category_detail_success_example,
                ),
            ],
        ),
        404: OpenApiResponse(
            description="Category not found.",
        ),
        500: OpenApiResponse(
            description="Internal server error.",
            examples=[
                OpenApiExample(
                    "Server error",
                    value=category_server_error_example,
                ),
            ],
        ),
    },
    tags=["Categories"],
)
