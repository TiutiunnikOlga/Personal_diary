from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Аватар', blank=True, null=True,
                               help_text='Введите аватар')
    phone = models.CharField(max_length=35, verbose_name='Телефон', blank=True, null=True,
                             help_text='Ваш номер телефона')
    token = models.CharField(max_length=100, verbose_name='Token', blank=True, null=True)
    telegram_id = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Telegram ID"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"