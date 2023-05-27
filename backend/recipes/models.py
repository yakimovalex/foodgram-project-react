from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q
from users.models import User

from .validator import check_name


class Ingredient(models.Model):
    """Ингридиенты для рецептов."""
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=settings.LENGTH_OF_RECIPES,
        db_index=True,
        validators=[check_name],
        help_text='Введите название ингредиента')
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=settings.LENGTH_OF_RECIPES,
        help_text='Введите единицу измерения')

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        max_length=settings.LENGTH_OF_RECIPES, unique=True,
        validators=[check_name],
        help_text='Введите название тега')
    color = models.CharField(
        verbose_name='Цвет в HEX',
        max_length=7, unique=True,
        validators=[check_name],
        help_text='Выберите цвет, например #49B64E')
    slug = models.SlugField(
        verbose_name='Уникальный слаг',
        max_length=settings.LENGTH_OF_RECIPES, unique=True,
        help_text='Укажите уникальный слаг')

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        help_text='Автор рецепта')
#    ingredients = models.ManyToManyField(
#        Ingredient,
#        through='IngredientRecipe',
#        verbose_name='Ингредиент')
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Название тега',
        help_text='Выберите tag')
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Опишите приготовление рецепта')
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=settings.LENGTH_OF_RECIPES,
        help_text='Введите название рецепта',
        validators=[check_name],
        db_index=True)
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(1, 'Минимальное время приготовления')],
        help_text='Укажите время приготовления рецепта в минутах')
    image = models.ImageField(
        verbose_name='Картинка рецепта',
        upload_to='media/',
        help_text='Добавьте изображение рецепта')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)

    class Meta:
        ordering = ['-id']
        default_related_name = 'recipe'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author'],
                name='unique_recipe')]


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredients',
        verbose_name='Название рецепта',
        on_delete=models.CASCADE,
        help_text='Выберите рецепт')
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='+',
        on_delete=models.CASCADE,
        help_text='Укажите ингредиенты')
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Минимальное количество ингредиентов 1')],
        verbose_name='Количество',
        help_text='Укажите количество ингредиента')

    class Meta:
        verbose_name = 'Cостав рецепта'
        verbose_name_plural = 'Состав рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredients')]

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class ShoppingCart(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        related_name='+',
        verbose_name='Рецепт для приготовления',
        on_delete=models.CASCADE,
        help_text='Выберите рецепт для приготовления')

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [models.UniqueConstraint(
            fields=['author', 'recipe'],
            name='unique_cart')]

    def __str__(self):
        return f'{self.recipe}'


class Favorite(models.Model):
    author = models.ForeignKey(
        User,

        on_delete=models.CASCADE,
        verbose_name='Автор рецепта')
    recipe = models.ForeignKey(
        Recipe,
        related_name='+',
        on_delete=models.CASCADE,
        verbose_name='Рецепты')

    class Meta:
        verbose_name = 'Избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [models.UniqueConstraint(
            fields=['author', 'recipe'],
            name='unique_favorite')]

    def __str__(self):
        return f'{self.recipe}'


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
