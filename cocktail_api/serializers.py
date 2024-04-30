from rest_framework import serializers
from base.models import Drink, DrinkRecipe, IngredientName, AlcoholType, FlavorProfile


class DrinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drink
        fields = ['drink_name', 'slug']


class DrinkRecipeSerializer(serializers.ModelSerializer):
    drink_name = serializers.StringRelatedField(source='drink.drink_name')
    slug = serializers.StringRelatedField(source='drink.slug')
    profile = serializers.ReadOnlyField(source='flavor_profile.profile')
    base_alcohol = serializers.StringRelatedField(many=True)
    ingredient_name = serializers.StringRelatedField(many=True)
    garnish = serializers.StringRelatedField(many=True)
    serving_glass = serializers.ReadOnlyField(source='serving_glass.name')
    mixing_direction = serializers.StringRelatedField()
    drink_type = serializers.StringRelatedField()
    must_know_drink = serializers.BooleanField()

    class Meta:
        model = DrinkRecipe
        fields = [
            'id', 'drink_name', 'slug', 'profile', 'base_alcohol', 'ingredient_name',
            'garnish', 'serving_glass', 'mixing_direction', 'drink_type', 'must_know_drink'
        ]

