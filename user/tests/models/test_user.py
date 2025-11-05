import pytest

from user.models import User
from user.tests.user_factory import AdminUserFactory, UserFactory


@pytest.mark.django_db
class TestUserModel:
    def test_create_normal_user(self):
        user = UserFactory()
        assert user.username
        assert user.email
        assert user.role == "USER"
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.check_password("defaultpassword123") is True

    def test_create_superuser(self):
        admin = AdminUserFactory()
        assert admin.role == "ADMIN"
        assert admin.is_staff is True
        assert admin.is_superuser is True
        assert admin.check_password("defaultpassword123") is True

    def test_username_required(self):
        with pytest.raises(ValueError, match="The Username field is required"):
            User.objects.create_user(username="", password="pass")
