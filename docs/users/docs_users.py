from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)

from docs.users.utils.examples import (
    delete_profile_success_example,
    login_invalid_example,
    login_request_example,
    login_success_example,
    logout_success_example,
    profile_permission_error_example,
    profile_success_example,
    register_conflict_example,
    register_request_example,
    register_success_example,
    update_profile_missing_error_example,
    update_profile_request_example,
    update_profile_success_example,
)
from users.serializers import (
    LoginSerializer,
    UserProfileUpdateSerializer,
    UserSerializer,
)

register_schema = extend_schema(
    summary="Register a new user",
    description=(
        "Creates a new user account with the provided details. "
        "Returns the created user."
    ),
    request=UserSerializer,
    responses={
        201: OpenApiResponse(
            response=None,
            description="User registered successfully.",
            examples=[
                OpenApiExample("Success", value=register_success_example),
            ],
        ),
        400: OpenApiResponse(
            description="Validation error or user already exists.",
            examples=[
                OpenApiExample(
                    "Username taken",
                    value=register_conflict_example,
                ),
                OpenApiExample(
                    "Validation error",
                    value=update_profile_missing_error_example,
                ),
            ],
        ),
    },
    examples=[
        OpenApiExample("Register request", value=register_request_example),
    ],
    tags=["Users"],
)

login_schema = extend_schema(
    summary="Login user",
    description="Authenticates a user and returns their profile.",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            description="Login successful.",
            examples=[OpenApiExample("Success", value=login_success_example)],
        ),
        400: OpenApiResponse(
            description="Validation error.",
            examples=[
                OpenApiExample(
                    "Missing credentials",
                    value=update_profile_missing_error_example,
                ),
            ],
        ),
        401: OpenApiResponse(
            description="Invalid credentials.",
            examples=[
                OpenApiExample("Invalid login", value=login_invalid_example),
            ],
        ),
    },
    examples=[OpenApiExample("Login request", value=login_request_example)],
    tags=["Users"],
)

profile_retrieve_schema = extend_schema(
    summary="Get user profile",
    description="Retrieve the authenticated user's profile.",
    responses={
        200: OpenApiResponse(
            description="Profile retrieved.",
            examples=[
                OpenApiExample("Success", value=profile_success_example),
            ],
        ),
        403: OpenApiResponse(
            description="Permission denied.",
            examples=[
                OpenApiExample(
                    "Forbidden",
                    value=profile_permission_error_example,
                ),
            ],
        ),
    },
    tags=["Users"],
)

profile_update_schema = extend_schema(
    summary="Update user profile",
    description="Update the authenticated user's profile.",
    request=UserProfileUpdateSerializer,
    responses={
        200: OpenApiResponse(
            description="Profile updated.",
            examples=[
                OpenApiExample(
                    "Success",
                    value=update_profile_success_example,
                ),
            ],
        ),
        400: OpenApiResponse(
            description="Validation error.",
            examples=[
                OpenApiExample(
                    "Missing fields",
                    value=update_profile_missing_error_example,
                ),
            ],
        ),
        403: OpenApiResponse(
            description="Permission denied.",
            examples=[
                OpenApiExample(
                    "Forbidden",
                    value=profile_permission_error_example,
                ),
            ],
        ),
    },
    examples=[
        OpenApiExample("Update request", value=update_profile_request_example),
    ],
    tags=["Users"],
)

profile_delete_schema = extend_schema(
    summary="Delete user profile",
    description="Deletes the authenticated user account.",
    responses={
        200: OpenApiResponse(
            description="Profile deleted.",
            examples=[
                OpenApiExample(
                    "Deleted",
                    value=delete_profile_success_example,
                ),
            ],
        ),
        403: OpenApiResponse(
            description="Permission denied.",
            examples=[
                OpenApiExample(
                    "Forbidden",
                    value=profile_permission_error_example,
                ),
            ],
        ),
    },
    tags=["Users"],
)

logout_schema = extend_schema(
    summary="Logout user",
    description="Log the user out of the current session.",
    responses={
        200: OpenApiResponse(
            description="Logout successful.",
            examples=[OpenApiExample("Success", value=logout_success_example)],
        ),
    },
    tags=["Users"],
)
