from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField("Номер телефона", max_length=12)
    telegram_username = models.CharField("Username пользователя в телеграм", default="")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_user_permissions",
        blank=True
    )
