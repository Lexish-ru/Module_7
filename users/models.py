from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя.
    Авторизация по email вместо username.
    Дополнительные поля: телефон, город, аватар.
    """
    username = None
    email = models.EmailField('email address', unique=True)
    phone = models.CharField('phone', max_length=20, blank=True)
    city = models.CharField('city', max_length=50, blank=True)
    avatar = models.ImageField('avatar', upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        """
        Возвращает строковое представление пользователя — email.
        """
        return self.email
