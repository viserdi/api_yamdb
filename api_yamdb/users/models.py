from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class NewUser(UserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Вы не заполнили email')
        if username == 'me':
            raise ValueError('Нельзя использовать username "me"')
        return super().create_user(
            username, email=email, password=password, **extra_fields
        )

    def create_superuser(
            self, username, email, password, role='admin', **extra_fields
    ):
        return super().create_superuser(
            username, email, password, role='admin', **extra_fields
        )


class User(AbstractUser):
    ROLES = (
        ('admin', 'admin'),
        ('moderator', 'moderator'),
        ('user', 'user'),
    )
    username = models.CharField(
        max_length=200,
        unique=True,
        db_index=True
    )
    role = models.CharField(
        verbose_name='Статус пользователя',
        max_length=100,
        choices=ROLES,
        default='user',
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    objects = NewUser()

    REQUIRED_FIELDS = ('email', 'password',)

    class Meta:
        ordering = ('id',)

    @property
    def is_admin(self):
        if self.role == 'admin':
            return True

    @property
    def is_moderator(self):
        if self.role == 'moderator':
            return True
