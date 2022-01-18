from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('admin', 'admin'),
        ('moderator', 'moderator'),
        ('user', 'user'),
    )
    role = models.CharField(
        verbose_name='Статус пользователя',
        max_length=100,
        choices=ROLES,
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
