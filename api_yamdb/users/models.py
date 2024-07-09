"""
Users app models configuration
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """CustomUser model class"""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    CUSTOM_USER_ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    role = models.CharField(
        verbose_name='User Role',
        choices=CUSTOM_USER_ROLE_CHOICES,
        default=USER,
        max_length=16,
    )

    username = models.CharField(
        verbose_name='Username',
        max_length=150,
        unique=True,)

    email = models.EmailField(
        verbose_name='Email',
        max_length=254,
        unique=True,)

    first_name = models.CharField(
        verbose_name='First Name',
        max_length=150,
        blank=True,)

    last_name = models.CharField(
        verbose_name='Last Name',
        max_length=150,
        blank=True,)

    bio = models.TextField(
        verbose_name='User biography',
        blank=True,)

    confirmation_code = models.CharField(
        verbose_name='Confirmation Code',
        max_length=64,
        editable=False,
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', ]

    @property
    def is_admin_or_super_user(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
