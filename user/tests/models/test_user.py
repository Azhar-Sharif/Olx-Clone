import pytest

from user.models import User


@pytest.mark.django_db
class TestUserModel:
    """Simple tests for User model and UserManager"""

    def test_create_normal_user(self):
        user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="mypassword123",
        )
        assert user.username == "alice"
        assert user.email == "alice@example.com"
        assert user.role == "USER"
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.check_password("mypassword123") is True

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass"
        )
        assert admin.username == "admin"
        assert admin.role == "ADMIN"
        assert admin.is_staff is True
        assert admin.is_superuser is True
        assert admin.check_password("adminpass") is True

    def test_username_required(self):
        with pytest.raises(ValueError, match="The Username field is required"):
            User.objects.create_user(username="", password="pass")
