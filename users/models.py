from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


# Кастомный менеджер пользователя
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и возвращает пользователя с email и паролем.
        """
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и возвращает суперпользователя с email и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    name = models.CharField(verbose_name='Имя', max_length=30, **NULLABLE)
    email = models.EmailField(verbose_name='Почта', unique=True)
    phone = models.CharField(max_length=13, unique=True, verbose_name="Телефон")

    token_auf = models.CharField(max_length=255, **NULLABLE, verbose_name='Токен')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.name}"

    @property
    def detailed_info(self):
        return (f"Имя: {self.name}, Почта: {self.email}, Телефон:{self.phone}, "
                f"{'Активен' if self.is_active else 'Не активен'}")
