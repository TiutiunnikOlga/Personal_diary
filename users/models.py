import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


def generate_token():
    return uuid.uuid4().hex


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Введите аватар",
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Ваш номер телефона",
    )
    token = models.CharField(
        max_length=100, verbose_name="Token", blank=True, null=True
    )
    is_email_confirmed = models.BooleanField(
        default=False, verbose_name="Email подтверждён"
    )
    email_confirmation_token = models.CharField(
        max_length=32,
        default=generate_token,
        editable=False,
        unique=True,
        verbose_name="Токен подтверждения",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
