from django.shortcuts import render, redirect, get_object_or_404
from base.models import (DrinkRecipe, Ingredient, Garnish, AlcoholType, Drink, ServingGlass, FlavorProfile)
from cocktail_api.serializers import DrinkRecipeSerializerV1
from django.http import JsonResponse, HttpResponse
from django.core import serializers
import json
from django.core.cache import cache
from datetime import date
from rest_framework import generics
from cocktail_api.views import MostPopularV1
from .forms import APIEndpointForm
import requests
import logging
import random
from rest_framework.response import Response
from django.core import serializers


from rest_framework.permissions import (
    SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission,
    IsAdminUser, DjangoModelPermissionsOrAnonReadOnly, AllowAny)

logging.basicConfig(filename='home_page.log', level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


# Create your views here.
def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


def home_page(request):
    today = date.today()
    year = today.year

    # Check for raw JSON toggle
    show_raw_json_on_page = request.GET.get('show_raw_json_on_page', 'no') == 'yes'

    show_raw_json = request.GET.get('show_raw_json', 'no') == 'yes'
    # Check if data is already in session
    api_response_data = request.session.get('api_response_data', None)

    # If not cached, fetch from API
    if not api_response_data:
        try:
            api_response = requests.get('https://www.drinksapi.paulrblack.com/api/v1/most-popular')
            api_response_data = api_response.json()
            request.session['api_response_data'] = api_response_data  # Cache data
        except Exception as e:
            logging.error(f'Error fetching data: {str(e)}')
            return render(request, 'home/home.html', {'error_message': f'Error fetching data: {str(e)}'})

    #  Process and display data in standard view
    if len(api_response_data['drinks']) > 0:
        current_drink_id = request.POST.get('current_drink_id', None)
        available_drinks = [drink for drink in api_response_data['drinks']['results'] if
                            drink['id'] != current_drink_id]

        if len(available_drinks) == 0:
            available_drinks = api_response_data['drinks']['results']

        random_drink = random.choice(available_drinks)
        data = {
            "id": random_drink['id'],
            "drink_name": random_drink['drink_name'],
            "slug": random_drink['slug'],
            "profile": random_drink['profile'],
            "base_alcohol": random_drink['base_alcohol'][0],
            "ingredient_name": random_drink['ingredients'],
            "garnish": random_drink['garnish'],
            "serving_glass": random_drink['serving_glass'],
            "mixing_direction": random_drink['mixing_direction'],
            "drink_type": random_drink['drink_type'],
            "must_know_drink": random_drink['must_know_drink'],
        }

        # If raw JSON view is requested
        if show_raw_json_on_page:
            print('year: show_raw_json_on_page', year)
            return render(request, 'home/home.html', {'random_drink': data, 'year': year, 'show_raw_json_on_page': show_raw_json_on_page})

        elif show_raw_json and not show_raw_json_on_page:
            print('year: show_raw_json', year)
            return JsonResponse(data)

        print('year:', year)
        return render(request, 'home/home.html', {'random_drink': data, 'year': year, 'show_raw_json_on_page': show_raw_json_on_page})

    return render(request, 'home/home.html', {'error_message': 'No popular drinks found'})


def about_page(request):
    today = date.today()
    year = today.year
    try:
        api_response = requests.get('https://www.drinksapi.paulrblack.com/api/v1/most-popular')
        api_response_data = api_response.json()
        available_drinks = api_response_data

        drinks = DrinkRecipe.objects.all()
        available_drinks_two = serializers.serialize('json', drinks)
        return render(request, 'about/about.html', {'year': year})
    except Exception as e:
        print(f'Exception: {e}')


def docs_page(request):
    today = date.today()
    year = today.year
    return render(request, 'docs/docs.html', {'year': year})