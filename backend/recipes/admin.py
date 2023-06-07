from django.contrib import admin

from users.models import Follow

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Tag)


class IngredientsInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 3


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    list_filter = ('author',)
    search_fields = ('user',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('author_recipe', 'recipe')
    list_filter = ('author_recipe',)
    search_fields = ('author_recipe',)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('author_recipe', 'recipe')
    list_filter = ('author_recipe',)
    search_fields = ('author_recipe',)


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount',)
    list_filter = ('recipe', 'ingredient')
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'pub_date', 'in_favorite', )
    search_fields = ('name',)
    list_filter = ('pub_date', 'author', 'name', 'tags')
    empty_value_display = '-пусто-'
    inlines = [IngredientsInline]

    def in_favorite(self, obj):
        return obj.favorite.all().count()

    in_favorite.short_description = 'Добавленные рецепты в избранное'


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    list_filter = ('name',)
    search_fields = ('name',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
