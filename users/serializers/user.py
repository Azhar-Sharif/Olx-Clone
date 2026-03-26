"""User serializers.

Provides serializers for user authentication, registration, and profile
updates.
"""

from rest_framework import serializers

from users.models import User


class LoginSerializer(serializers.Serializer):
    """Validates login credentials for the user authentication
    endpoint."""

    username = serializers.CharField(
        max_length=150,
        required=True,
        help_text="Enter your username",
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        help_text="Enter your password",
    )

    def validate(self, attrs):
        """Validates that username and password are present."""
        username = attrs.get("username")
        password = attrs.get("password")

        if not username or not password:
            raise serializers.ValidationError(
                "Username and password are required",
            )

        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Serializes user data for registration and read operations."""

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
        """Creates a new user with encrypted password."""
        return User.objects.create_user(**validated_data)


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializes user data for profile update operations."""

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
        """Updates user, properly hashing the password if it's
        provided."""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
