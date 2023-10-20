from rest_framework import serializers
from base.models import Drink, DrinkRecipe, IngredientName, AlcoholType, FlavorProfile


class DrinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drink
        fields = ['drink_name']


class FlavorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlavorProfile
        fields = ['profile']


class AlcoholTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlcoholType
        fields = ['spirit_type']


class IngredientNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientName
        fields = ['ingredient']


class DrinkRecipeSerializer(serializers.ModelSerializer):
    drink_name = serializers.ReadOnlyField(source='drink.drink_name')
    profile = serializers.ReadOnlyField(source='flavor_profile.profile')
    base_alcohol = serializers.StringRelatedField(many=True)
    ingredient_name = serializers.StringRelatedField(many=True)
    garnish = serializers.StringRelatedField(many=True)
    serving_glass = serializers.ReadOnlyField(source='serving_glass.name')
    mixing_direction = serializers.ReadOnlyField()

    class Meta:
        model = DrinkRecipe
        fields = [
            'id', 'drink_name', 'profile', 'base_alcohol', 'ingredient_name', 'garnish', 'serving_glass',
            'mixing_direction'
        ]

