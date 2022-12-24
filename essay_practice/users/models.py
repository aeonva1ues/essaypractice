from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(
        verbose_name='почта',
        max_length=255,
        unique=True
    )
    is_banned = models.BooleanField(
        verbose_name='заблокирован',
        default=False
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username
