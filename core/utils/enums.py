from enum import Enum


class SuccessMessages(Enum):
    PRODUCT_CREATED = "Product created successfully."
    PRODUCT_UPDATED = "Product updated successfully."
    PRODUCT_DELETED = "Product deleted successfully."
    OK = "OK"

    ORDER_PLACED = "Order placed successfully."
    ORDER_CANCELLED = "Order cancelled successfully."
    ORDER_PAID = "Order marked as paid."
    ORDER_SHIPPED = "Order shipped successfully."
    ORDER_DELIVERED = "Order delivered successfully."

    CATEGORY_RETRIEVED = "Category retrieved successfully."
    CATEGORY_LISTED = "Categories listed successfully."

    USER_CREATED = "User created successfully."
    USER_PROFILE_UPDATED = "User profile updated successfully."
    USER_PROFILE_DELETED = "User profile deleted successfully."
    USER_LOGGED_IN = "Login successful."
    USER_LOGGED_OUT = "Logged out successfully."


class ErrorMessages(Enum):
    PRODUCT_NOT_FOUND = "Requested product not found."
    VALIDATION_ERROR = "Validation error occurred."
    PERMISSION_DENIED = "Permission denied."
    SERVER_ERROR = "Internal server error."

    ORDER_NOT_FOUND = "Requested order not found."
    INVENTORY_NOT_AVAILABLE = (
        "Requested quantity for one or more products is not available."
    )

    NEGATIVE_PRICE = "Price must be zero or positive."

    CATEGORY_NOT_FOUND = "Requested category not found."

    USER_NOT_FOUND = "Requested user not found."
    INVALID_CREDENTIALS = "Invalid username or password."
    AUTH_REQUIRED = "Authentication required."
    USER_NAME_EMPTY = "Username cannot be empty."
    USERNAME_TAKEN = "Choose another Username."
