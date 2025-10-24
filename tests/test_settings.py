from django.conf import settings


def test_secret_key_exists():
    assert settings.SECRET_KEY
