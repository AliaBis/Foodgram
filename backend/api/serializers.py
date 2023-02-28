from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from rest_framework import exceptions, serializers
from api.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.serializers import CustomUserSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient."""
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели RecipeIngredient."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe. Чтение."""
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='recipeingredients',
        many=True
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time',)

    def get_is_favorited(self, obj):
        """Добавлен ли рецепт в Избранное."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """Добавлен ли рецепт в список Покупок."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()


class FavoriteShoppingSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Favorite и ShoppingCart."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления ингредиентов при создании рецепта."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        validators=[MinValueValidator(
            1,
            message='Количество должно быть равным или больше 1!'
        )
        ]
    )

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class RecipePostUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe. Создание, Обновление."""
    ingredients = IngredientForRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'author', 'image', 'name',
                  'text', 'cooking_time')

    def validate(self, data):
        """Проверка входящих данных на валидность."""
        cooking_time = data['cooking_time']
        ingredients = data['ingredients']
        tags = data['tags']
        if cooking_time <= 0:
            raise exceptions.ValidationError(
                'Время приготовления должно быть больше нуля!'
            )
        if len(ingredients) == 0:
            raise exceptions.ValidationError(
                'В рецепт не добавлены ингредиенты'
            )
        if len(ingredients) != len(set([item['id'] for item in ingredients])):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться!')
        ingredients = data['ingredients']
        for ingredient in ingredients:
            if not Ingredient.objects.filter(
                    id=ingredient['id']).exists():
                raise serializers.ValidationError({
                    'ingredients': f'Ингредиента с id - {ingredient["id"]} '
                                   f'нет в базе'
                })
        if len(tags) != len(set([item for item in tags])):
            raise serializers.ValidationError({
                'tags': 'Теги не должны повторяться!'})

        return data

    def add_ingredient_tag(self, ingredients, tags, recipe):
        """Добавление ингредиентов и тэгов в рецепт при создании и
        редактировании."""
        for tag in tags:
            recipe.tags.add(tag)
            recipe.save()
        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=recipe,
                ingredient_id=ingredient['id'],
                amount=ingredient['amount'], )
            for ingredient in ingredients
        ])
        return recipe

    def create(self, validated_data):
        """Создание нового рецепта."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        return self.add_ingredient_tag(ingredients, tags, recipe)

    def update(self, instance, validated_data):
        """Обновление рецепта."""
        instance.ingredients.clear()
        instance.tags.clear()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        super().update(instance, validated_data)
        return self.add_ingredient_tag(ingredients, tags, instance)

    def to_representation(self, value):
        """Выбор сериализатора для вывода результата работы класса."""
        serializer = RecipeSerializer(value, context=self.context)
        return serializer.data
