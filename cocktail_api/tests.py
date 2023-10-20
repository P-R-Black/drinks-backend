from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from base.models import (IngredientName, Garnish, AlcoholType, Drink, ServingGlass, FlavorProfile, DrinkRecipe)


class PostTests(APITestCase):

    def test_view_post(self):
        url = reverse('cocktail_api:listcreate')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)




