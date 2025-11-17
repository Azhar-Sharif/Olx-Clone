from rest_framework import serializers

from users.models import User


class LoginSerializer(serializers.Serializer):
    """Serializer for user login.

    Request body example:
    {
        "username": "johndoe",
        "password": "secret123"
    }

    Success response (api_response wrapper) example:
    {
      "success": true,
      "message": "User logged in successfully.",
      "data": {"id": 1, "username": "johndoe", "email": "..."},
      "errors": null
    }

    Error response example (validation):
    {
      "success": false,
      "message": "Validation error occurred.",
      "data": null,
      "errors": {"username": ["This field is required."]}
    }
    """

    username = serializers.CharField(
        max_length=150, required=True, help_text="Enter your username"
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        help_text="Enter your password",
    )

    def validate(self, attrs):
        """Validate credentials"""
        username = attrs.get("username")
        password = attrs.get("password")

        if not username or not password:
            raise serializers.ValidationError(
                "Username and password are required"
            )

        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user registration and representation.

    Request body example (registration):
    {
      "username": "johndoe",
      "email": "john@example.com",
      "password": "secret123",
      "first_name": "John",
      "last_name": "Doe"
    }

    Success response (api_response wrapper) example:
    {
      "success": true,
      "message": "User created successfully.",
      "data": { ...user fields... },
      "errors": null
    }
    """

    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={"input_type": "password"},
        help_text="Password must be at least 8 characters long",
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone_no",
            "address",
            "password",
        ]
        read_only_fields = ["id", "role"]

    def create(self, validated_data):
        """Create a new user with encrypted password"""
        return User.objects.create_user(**validated_data)


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer used for updating the authenticated user's profile.

    Request example:
    {
      "email": "new@example.com",
      "first_name": "New",
      "password": "newpass123"
    }

    Success response (api_response wrapper) example:
    {
      "success": true,
      "message": "OK",
      "data": { ...updated user... },
      "errors": null
    }
    """

    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8,
        style={"input_type": "password"},
        help_text="Password must be at least 8 characters long",
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone_no",
            "address",
            "password",
        ]
        read_only_fields = ["id", "username", "role"]

    def update(self, instance, validated_data):
        """Update user, properly hashing the password if it's provided."""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
