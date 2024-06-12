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
from .forms import APIEndpointForm

import requests


# Create your views here.
def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


def home_page(request):
    today = date.today()
    year = today.year

    most_popular = DrinkRecipe.objects.filter(top_hundred_drink=True)
    api_length = len(most_popular)

    form = APIEndpointForm(request.POST or None)
    if is_ajax(request):
        if form.is_valid():
            endpoint_name = form.cleaned_data['endpoint_name']
            api_response = requests.get(f'http://127.0.0.1:8000/api/most-popular/{endpoint_name}')
            data = api_response.json()
            return JsonResponse({'data': data})
        else:
            api_response = requests.get('http://127.0.0.1:8000/api/most-popular/')
            data = api_response.json()
            return JsonResponse({'data': data})

    return render(request, 'home/home.html', {'year': year, 'form': form, 'api_length': api_length})


def about_page(request):
    return render(request, 'about/about.html')


def docs_page(request):
    return render(request, 'docs/docs.html')
