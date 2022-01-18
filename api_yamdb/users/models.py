from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CHOICES = (
        ('admin', 'admin'),
        ('moderator', 'moderator'),
        ('user', 'user'),
    )
    role = models.CharField(
        max_length=100,
        choices=CHOICES,
        blank=True,
    )
