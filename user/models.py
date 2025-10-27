from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import UserManager


class User(AbstractUser):
    ROLE_Choices = (
        ("USER", "User"),
        ("ADMIN", "Admin"),
    )

    role = models.CharField(choices=ROLE_Choices, default="USER")
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    objects = UserManager()

    def __str__(self):
        return f"{self.username}({self.role})"
