from rest_framework.response import Response
from rest_framework  import generics
from rest_framework.decorators import api_view
from base.models import Drink, DrinkRecipe
from .serializers import DrinkSerializer, DrinkRecipeSerializer


class DrinkList(generics.ListAPIView):
    queryset = DrinkRecipe.drinkobjects.all()
    serializer_class = DrinkRecipeSerializer


class DrinkDetail(generics.RetrieveAPIView):
    queryset = DrinkRecipe.objects.all()
    serializer_class = DrinkRecipeSerializer


# @api_view(['GET'])
# def get_data(request):
#     drink_recipe = DrinkRecipe.objects.all()
#     serializer = DrinkRecipeSerializer(drink_recipe, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['POST'])
# def add_item(request):
#     serializer = DrinkSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)