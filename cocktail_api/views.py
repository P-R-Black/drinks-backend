from rest_framework.permissions import (SAFE_METHODS, IsAdminUser,
                                        BasePermission, DjangoModelPermissionsOrAnonReadOnly)
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from base.models import Drink, DrinkRecipe
from .serializers import DrinkSerializer, DrinkRecipeSerializer, AlcoholTypeSerializer


class UserWritePermission(BasePermission):
    message = "Editing Drink Data is Restriced to Admin Only"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user


class DrinkDetail(generics.RetrieveUpdateDestroyAPIView, UserWritePermission):
    # permission_classes = [IsAdminUser]
    queryset = DrinkRecipe.objects.all()
    serializer_class = DrinkRecipeSerializer


class DrinkList(generics.ListAPIView):
    # permission_classes = [IsAdminUser]
    queryset = DrinkRecipe.drinkobjects.all()
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