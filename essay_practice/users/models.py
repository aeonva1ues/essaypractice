from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    email = models.EmailField(
        verbose_name='Почта',
        max_length=255,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
