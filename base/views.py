from django.shortcuts import render, redirect, get_object_or_404
from base.models import (
    DrinkRecipe, IngredientName, Garnish, AlcoholType,
                         Drink, ServingGlass, FlavorProfile)
from cocktail_api.serializers import DrinkSerializer, DrinkRecipeSerializer
from django.http import JsonResponse
from django.core import serializers
import json
from django.core.cache import cache
from datetime import date
from rest_framework import generics
from cocktail_api.views import MostPopular


# Create your views here.
def home_page(request):
    today = date.today()
    year = today.year
    return render(request, 'home/home.html', {'year': year})


def about_page(request):
    return render(request, 'about/about.html')


def docs_page(request):
    return render(request, 'docs/docs.html')

