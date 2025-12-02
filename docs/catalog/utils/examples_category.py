category_example = {
    "id": 1,
    "category_name": "Electronics",
}

category_list_success_example = {
    "success": True,
    "message": "Categories listed successfully.",
    "data": [category_example],
    "errors": None,
}

category_detail_success_example = {
    "success": True,
    "message": "Category retrieved successfully.",
    "data": category_example,
    "errors": None,
}
category_list_empty_success_example = {
    "success": True,
    "message": "Categories listed successfully.",
    "data": [],
    "errors": None,
}

category_server_error_example = {
    "success": False,
    "message": "Internal server error.",
    "data": None,
    "errors": {"detail": "Server error."},
}
