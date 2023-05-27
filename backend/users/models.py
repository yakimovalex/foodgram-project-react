from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from recipes.validator import check_name


class User(AbstractUser):
    username = models.CharField('Логин',
                                max_length=settings.LENGTH_OF_NAME,
                                validators=[check_name], unique=True)
    first_name = models.CharField('Имя',
                                  max_length=settings.LENGTH_OF_NAME,
                                  validators=[check_name])
    last_name = models.CharField('Фамилия',
                                 max_length=settings.LENGTH_OF_NAME,
                                 validators=[check_name])
    email = models.EmailField('email-адрес', unique=True)
    password = models.CharField('Пароль', max_length=settings.LENGTH_OF_NAME)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
