from django.db import models
from django.db.models import CASCADE

from users.models import User


class Entries(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, verbose_name='Пользователь', related_name='entries')
    heading = models.CharField(max_length=255, verbose_name='Заголовок', help_text='Введите название заголовка')
    content = models.TextField(verbose_name='Содержимое', help_text='Введите содержимое')
    photo = models.ImageField(upload_to='entries/photo', blank=True, null=True, verbose_name='Фото',
                              help_text='Добавьте фото')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Мой дневник"
        verbose_name_plural = "Мои дневники"
        ordering = [
            'created_at'
        ]

    def __str__(self):
        return self.heading
