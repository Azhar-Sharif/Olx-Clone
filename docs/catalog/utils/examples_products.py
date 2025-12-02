product_example = {
    "id": 1,
    "product_name": "iPhone 15",
    "quantity": 10,
    "description": "Latest model smartphone",
    "price": "1499.99",
    "product_img": None,
    "product_img_url": "https://example.com/media/products/iphone15.jpg",
    "created_at": "2025-01-01T12:00:00Z",
    "user": 1,
    "user_name": "alice",
    "category": 1,
    "category_name": "Electronics",
}

product_list_success_example = {
    "success": True,
    "message": "Products listed successfully.",
    "data": [product_example],
    "errors": None,
}

product_list_empty_success_example = {
    "success": True,
    "message": "Products retrieved successfully.",
    "data": [],
    "errors": None,
}


product_detail_success_example = {
    "success": True,
    "message": "Products retrieved successfully.",
    "data": product_example,
    "errors": None,
}

product_create_request_example = {
    "product_name": "iPhone 15",
    "quantity": 10,
    "description": "Latest model smartphone",
    "price": "1499.99",
    "category": 1,
}


product_create_success_example = {
    "success": True,
    "message": "Product created successfully.",
    "data": product_example,
    "errors": None,
}

product_update_request_example = {
    "product_name": "iPhone 15 Pro",
    "quantity": 5,
    "description": "Updated model smartphone",
    "price": "1599.99",
    "category": 1,
}

product_partial_update_request_example = {
    "price": "1399.99",
}

product_validation_error_example = {
    "success": False,
    "message": "Validation error occurred.",
    "data": None,
    "errors": {"price": ["Price must be zero or positive."]},
}

product_auth_required_example = {
    "success": False,
    "message": "Authentication required.",
    "data": None,
    "errors": {"detail": "Authentication credentials were not provided."},
}

product_permission_denied_example = {
    "success": False,
    "message": "Permission denied.",
    "data": None,
    "errors": {"detail": "You do not have permission to perform this action."},
}

product_not_found_example = {
    "success": False,
    "message": "Requested product not found.",
    "data": None,
    "errors": {"detail": "Not found."},
}

product_server_error_example = {
    "success": False,
    "message": "Internal server error.",
    "data": None,
    "errors": {"detail": "Server error."},
}
