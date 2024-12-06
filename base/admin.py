from django.contrib import admin
from .models import Drink, Ingredient, DrinkRecipe, AlcoholType, ServingGlass, Garnish, FlavorProfile


@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    model = Drink


@admin.register(Ingredient)
class IngredientNameAdmin(admin.ModelAdmin):
    model = Ingredient


@admin.register(DrinkRecipe)
class DrinkRecipeAdmin(admin.ModelAdmin):
    model = DrinkRecipe

    list_display = ('drink', 'mixing_direction',)
    list_filter = ('drink', 'flavor_profile', 'base_alcohol',)
    search_fields = ('drink', 'base_alcohol',)


@admin.register(AlcoholType)
class AlcoholTypeAdmin(admin.ModelAdmin):
    model = AlcoholType


@admin.register(ServingGlass)
class ServingGlassAdmin(admin.ModelAdmin):
    model = ServingGlass


@admin.register(Garnish)
class GarnishAdmin(admin.ModelAdmin):
    model = Garnish

    list_display = ('name', 'measurement', 'value',)


@admin.register(FlavorProfile)
class FlavorProfileAdmin(admin.ModelAdmin):
    model = FlavorProfile
