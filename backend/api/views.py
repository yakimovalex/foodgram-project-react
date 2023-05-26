from api.filters import IngredientSearchFilter, RecipeFilter
from api.paginations import ApiPagination
from api.permissions import IsOwnerOrAdminOrReadOnly
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeListSerializer, RecipeWriteSerializer,
                             ShoppingCartSerializer, TagSerializer)
from api.services import shopping_cart
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, Recipe, ShoppingCart, Tag,
                            User)
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """Теги."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """Ингредиенты."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    filter_backends = (IngredientSearchFilter, )
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Recipe: [GET, POST, DELETE, PATCH]."""
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    pagination_class = ApiPagination
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeListSerializer
        return RecipeWriteSerializer

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, *args, **kwargs):
        """
        Корректировка списка избранного пользователя
        Получить / Добавить / Удалить рецепт.
        """
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        user = self.request.user
        if request.method == 'POST':
            if Favorite.objects.filter(author=user,
                                       recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже записан!'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = FavoriteSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(author=user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        if not Favorite.objects.filter(author=user,
                                       recipe=recipe).exists():
            return Response({'errors': 'Пусто'},
                            status=status.HTTP_404_NOT_FOUND)
        Favorite.objects.get(recipe=recipe).delete()
        return Response('Рецепт удалён из списка избранного.',
                        status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, **kwargs):
        """
        Изменение списка покупок пользоватля
        Получить / Добавить / Удалить.
        """
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        user = self.request.user
        if request.method == 'POST':
            if ShoppingCart.objects.filter(author=user,
                                           recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже добавлен!'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = ShoppingCartSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(author=user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        if not ShoppingCart.objects.filter(author=user,
                                           recipe=recipe).exists():
            return Response({'errors': 'Объект не найден'},
                            status=status.HTTP_404_NOT_FOUND)
        ShoppingCart.objects.get(recipe=recipe).delete()
        return Response('Рецепт успешно удалён из списка покупок.',
                        status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """
        Скачать общий список покупок для выбранных рецептов
        """
        author = User.objects.get(id=self.request.user.pk)
        if author.shopping_cart.exists():
            return shopping_cart(self, request, author)
        return Response('Список покупок пустой.',
                        status=status.HTTP_404_NOT_FOUND)
