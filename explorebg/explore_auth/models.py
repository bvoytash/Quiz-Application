from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, PermissionsMixin
from django.db import models

from explorebg.explore_auth.manager import ExploreUserManager


class ExploreUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    objects = ExploreUserManager()


class Profile(models.Model):
    username = models.CharField(
        max_length=15,
        blank=True,
        null=True,
    )

    user = models.OneToOneField(
        ExploreUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )


from .signals import *
