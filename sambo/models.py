from __future__ import annotations

import secrets
import string
import typing as t

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager["User"]):
    def create_superuser(self, *, email: str, password: str, **extra_fields: t.Any) -> User:
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create(
            email=email,
            password=make_password(password),
            is_superuser=True,
            is_active=True,
        )


class User(AbstractBaseUser):
    email = models.EmailField("mejladress", unique=True)
    is_active = models.BooleanField("är aktiv")
    is_superuser = models.BooleanField("är superadmin")

    class Meta:
        verbose_name = "användare"
        verbose_name_plural = "användare"

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS: t.ClassVar[list[str]] = []

    is_staff = True  # Allow access to admin

    def set_random_password(self) -> str:
        password = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))
        self.set_password(password)
        return password

    def has_perm(self, perm: str, obj: models.Model | None = None) -> bool:
        assert self.is_active

        if self.is_superuser:
            return True

        valid_perms = (
            "todo_list",
            "todo_item",
        )

        if perm not in valid_perms:
            return False

        return True

    def has_module_perms(self, app_label: str) -> bool:
        assert self.is_active

        if self.is_superuser:
            return True

        return app_label in ("sambo",)

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
