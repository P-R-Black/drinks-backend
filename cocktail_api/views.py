from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly,
                                        BasePermission, IsAdminUser, DjangoModelPermissionsOrAnonReadOnly)
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import filters
from base.models import Drink, DrinkRecipe, AlcoholType
from .serializers import DrinkSerializer, DrinkRecipeSerializer
from django.shortcuts import get_object_or_404
from django.utils.text import slugify


class UserWritePermission(BasePermission):
    message = "Editing Drink Data is Restriced to Admin Only"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user


# class DrinkList(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = DrinkRecipeSerializer
#     queryset = DrinkRecipe.drinkobjects.all()

    # def get_object(self, queryset=None, **kwargs):
    #     item = self.kwargs.get('pk')
    #     return get_object_or_404(DrinkRecipe, id=item)
    #
    # # Define Custom Queryset
    # def get_queryset(self):
    #     return DrinkRecipe.objects.all()


# class DrinkList(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = DrinkRecipe.drinkobjects.all()
#
#     def list(self, request):
#         print('request list', request)
#         serializer_class = DrinkRecipeSerializer(self.queryset, many=True)
#         print('serializer_class list', request)
#         return Response(serializer_class.data)
#
#     def retrieve(self, request, pk=None):
#         print('request retrieve', request)
#         drink_recipe = get_object_or_404(self.queryset, pk=pk)
#         print('drink_recipe retrieve', request)
#         serializer_class = DrinkRecipeSerializer(drink_recipe)
#         return Response(serializer_class.data)






class DrinkList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = DrinkRecipe.drinkobjects.all()
    serializer_class = DrinkRecipeSerializer


class DrinkDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [UserWritePermission]
    queryset = DrinkRecipe.objects.all()
    serializer_class = DrinkRecipeSerializer


class BaseDrink(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = DrinkRecipeSerializer

    def get_queryset(self, **kwargs):

        base = slugify(self.kwargs.get('drink'))
        base_alc_two = AlcoholType.objects.all()
        print('base', base)
        for item in base_alc_two.values():
            print("item['spirit_type']", item['spirit_type'])
            if slugify(item['spirit_type']) == base:
                item_lookup = item['id']
                print('item_lookup', item_lookup)
                return DrinkRecipe.objects.filter(base_alcohol=item_lookup)

        return DrinkRecipe.objects.all()


class MustKnows(generics.ListCreateAPIView):
    serializer_class = DrinkRecipeSerializer

    def get_queryset(self):
        must_knows = DrinkRecipe.objects.filter(must_know_drink=True)
        return must_knows

# Some Generic Options
# RetrieveUpdateDestroyAPIView
# ListCreateAPIView
# RetrieveAPIView
# ListAPIView



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