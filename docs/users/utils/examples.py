user_data_example = {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "first_name": "Alice",
    "last_name": "Smith",
    "role": "USER",
    "phone_no": "+123456789",
    "address": "123 Main St",
}

register_request_example = {
    "username": "alice",
    "email": "alice@example.com",
    "first_name": "Alice",
    "last_name": "Smith",
    "phone_no": "+123456789",
    "address": "123 Main St",
    "password": "some_strong_password",
}
register_success_example = {
    "success": True,
    "message": "User created successfully.",
    "data": user_data_example,
    "errors": None,
}
register_conflict_example = {
    "success": False,
    "message": "Choose another Username.",
    "data": None,
    "errors": {"username": ["A user with that username already exists."]},
}

login_request_example = {
    "username": "alice",
    "password": "some_strong_password",
}
login_success_example = {
    "success": True,
    "message": "Login successful.",
    "data": user_data_example,
    "errors": None,
}
login_invalid_example = {
    "success": False,
    "message": "Invalid credentials.",
    "data": None,
    "errors": {"detail": "Invalid username or password."},
}

profile_success_example = {
    "success": True,
    "message": "OK",
    "data": user_data_example,
    "errors": None,
}
update_profile_request_example = {
    "email": "alice.new@example.com",
    "first_name": "Alice",
    "last_name": "Johnson",
    "phone_no": "+987654321",
    "address": "456 Side St",
    "password": "new_password123",
}
update_profile_success_example = {
    "success": True,
    "message": "Profile updated",
    "data": {
        **user_data_example,
        "email": "alice.new@example.com",
        "last_name": "Johnson",
    },
    "errors": None,
}
update_profile_missing_error_example = {
    "success": False,
    "message": "Validation failed",
    "data": None,
    "errors": {"email": ["This field is required."]},
}
profile_permission_error_example = {
    "success": False,
    "message": "Permission denied",
    "data": None,
    "errors": {"detail": "You do not have permission to perform this action."},
}

delete_profile_success_example = {
    "success": True,
    "message": "Profile deleted",
    "data": None,
    "errors": None,
}

logout_success_example = {
    "success": True,
    "message": "Logged out successfully.",
    "data": None,
    "errors": None,
}
