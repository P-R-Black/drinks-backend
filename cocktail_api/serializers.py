from rest_framework import serializers
from base.models import DrinkRecipe, Drink, Ingredient, Garnish, AlcoholType, ServingGlass, FlavorProfile


class DrinkRecipeSerializerV1(serializers.ModelSerializer):
    drink_name = serializers.CharField(source='drink.name')
    slug = serializers.CharField(source='drink.slug')
    profile = serializers.CharField(source='flavor_profile.profile', allow_null=True)
    base_alcohol = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    ingredients = serializers.StringRelatedField(many=True)
    garnish = serializers.SerializerMethodField()
    serving_glass = serializers.CharField(source='serving_glass.name')
    mixing_direction = serializers.CharField()
    drink_type = serializers.CharField()
    must_know_drink = serializers.BooleanField()

    class Meta:
        model = DrinkRecipe
        fields = [
            'id', 'drink_name', 'slug', 'profile', 'base_alcohol', 'ingredients', 'garnish', 'slug',
            'serving_glass', 'mixing_direction', 'drink_type', 'must_know_drink',
        ]

    def get_garnish(self, obj):
        return ['{} {}'.format(garnish.value, garnish.name) for garnish in obj.garnish.all()]


class AlcoholTypeSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = AlcoholType
        fields = ['name', 'slug']