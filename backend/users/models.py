from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q
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
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='follower',
        on_delete=models.CASCADE,
        help_text='Текущий пользователь')
    author = models.ForeignKey(
        User,
        verbose_name='Подписка',
        related_name='followed',
        on_delete=models.CASCADE,
        help_text='Подписаться на автора рецепта(ов)')

    class Meta:
        verbose_name = 'Мои подписки'
        verbose_name_plural = 'Мои подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_following'),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='no_self_following')]

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.author}'
