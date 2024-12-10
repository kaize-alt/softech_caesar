from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, email=None, **extra_fields):
        """
        Создаёт и возвращает обычного пользователя.
        """
        if not phone_number:
            raise ValueError('Необходимо указать номер телефона.')

        phone_number = phone_number.replace('+', '')

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, email=None, **extra_fields):
        """
        Создаёт и возвращает суперпользователя.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(phone_number, password, email, **extra_fields)


class CustomUser(AbstractUser):
    phone_number = models.CharField("Номер телефона", unique=True, max_length=12)
    address = models.CharField("Адрес", max_length=255, null=True, blank=True)
    telegram_username = models.CharField("Username пользователя в телеграм", default="")
    username = models.CharField("Username пользователя в телеграм", default="")
    USERNAME_FIELD = 'phone_number'
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователь"
