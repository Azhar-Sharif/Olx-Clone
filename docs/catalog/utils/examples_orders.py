order_products_example = [
    {
        "product_id": 1,
        "product_name": "iPhone 15",
        "quantity": 2,
        "unit_price": "1499.99",
    },
]

order_list_success_example = {
    "success": True,
    "message": "OK",
    "data": [
        {
            "id": 1,
            "user": "alice",
            "order_date": "2025-01-01T12:00:00Z",
            "products": order_products_example,
            "total_amount": "2999.98",
            "shipping_address": "123 Main St",
            "order_status": "PLACED",
        },
    ],
    "errors": None,
}

order_list_empty_success_example = {
    "success": True,
    "message": "OK",
    "data": [],
    "errors": None,
}

order_detail_success_example = {
    "success": True,
    "message": "OK",
    "data": {
        "id": 1,
        "user": "alice",
        "order_date": "2025-01-01T12:00:00Z",
        "products": order_products_example,
        "total_amount": "2999.98",
        "shipping_address": "123 Main St",
        "order_status": "PLACED",
    },
    "errors": None,
}


order_create_request_example = {
    "shipping_address": "123 Main St",
    "products_data": [
        {"product_id": 1, "quantity": 2},
        {"product_id": 2, "quantity": 1},
    ],
}

order_create_success_example = {
    "success": True,
    "message": "Order placed successfully.",
    "data": order_detail_success_example["data"],
    "errors": None,
}


order_update_request_example = {
    "shipping_address": "456 New Street",
}

order_update_success_example = {
    "success": True,
    "message": "OK",
    "data": {
        "id": 1,
        "user": "alice",
        "order_date": "2025-01-01T12:00:00Z",
        "products": order_products_example,
        "total_amount": "2999.98",
        "shipping_address": "456 New Street",
        "order_status": "PLACED",
    },
    "errors": None,
}

order_partial_update_request_example = {
    "shipping_address": "456 New Street",
}

order_partial_update_success_example = {
    "success": True,
    "message": "OK",
    "data": {
        "id": 1,
        "user": "alice",
        "order_date": "2025-01-01T12:00:00Z",
        "products": order_products_example,
        "total_amount": "2999.98",
        "shipping_address": "456 New Street",
        "order_status": "PLACED",
    },
    "errors": None,
}
order_inventory_error_example = {
    "success": False,
    "message": "Requested quantity for one or more products is not available.",
    "data": None,
    "errors": [
        "Inventory check failed: The quantity requested for product 1"
        " is not available.",
    ],
}

order_validation_error_example = {
    "success": False,
    "message": "Validation error occurred.",
    "data": None,
    "errors": {"products_data": ["This field is required."]},
}

order_auth_required_example = {
    "success": False,
    "message": "Authentication required.",
    "data": None,
    "errors": {"detail": "Authentication credentials were not provided."},
}

order_not_found_example = {
    "success": False,
    "message": "Requested order not found.",
    "data": None,
    "errors": {"detail": "Not found."},
}

order_permission_denied_example = {
    "success": False,
    "message": "Permission denied.",
    "data": None,
    "errors": {"detail": "You do not have permission to perform this action."},
}

order_server_error_example = {
    "success": False,
    "message": "Internal server error.",
    "data": None,
    "errors": {"detail": "Server error."},
}
