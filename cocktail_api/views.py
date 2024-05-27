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


class AllCocktails(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = DrinkRecipeSerializer

    def get_queryset(self):
        return DrinkRecipe.objects.filter(drink_type="cocktail")


class BaseDrink(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = DrinkRecipeSerializer

    def get_queryset(self, **kwargs):

        base = slugify(self.kwargs.get('base_alcohol'))
        base_alc_two = AlcoholType.objects.all()
        for item in base_alc_two.values():
            if slugify(item['spirit_type']) == base:
                item_lookup = item['id']
                return DrinkRecipe.objects.filter(base_alcohol=item_lookup)

        return DrinkRecipe.objects.all()


class MustKnows(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = DrinkRecipeSerializer

    def get_queryset(self):
        must_knows = DrinkRecipe.objects.filter(must_know_drink=True)
        return must_knows


class MostPopular(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = DrinkRecipeSerializer

    def get_queryset(self):
        most_popular = DrinkRecipe.objects.filter(top_hundred_drink=True)
        print('most_popular_length', len(most_popular))
        return most_popular


class ShotByBase(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = DrinkRecipeSerializer

    def get_queryset(self, **kwargs):
        base = slugify(self.kwargs.get('base_alcohol'))
        base_alc_two = AlcoholType.objects.all()
        for item in base_alc_two.values():
            if slugify(item['spirit_type']) == base:
                item_lookup = item['id']
                shot_by_base = DrinkRecipe.objects.filter(drink_type='shot', base_alcohol=item_lookup)
                print('shot_by_base', shot_by_base)
                return shot_by_base


class AllShots(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = DrinkRecipeSerializer

    def get_queryset(self):
        return DrinkRecipe.objects.filter(drink_type="shot")


class ShotRecipe(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = DrinkRecipeSerializer

    def get_queryset(self, **kwargs):
        base = slugify(self.kwargs.get('base_alcohol'))
        shot_name = slugify(self.kwargs.get('shot_name'))
        drink_id = 0
        for dro in Drink.objects.all().values():
            if slugify(dro['drink_name']) == shot_name:
                drink_id = dro['id']
                break

        base_alc_two = AlcoholType.objects.all()
        for item in base_alc_two.values():
            if slugify(item['spirit_type']) == base:
                item_lookup = item['id']
                shot_recipe = DrinkRecipe.objects.filter(
                    drink_type='shot',
                    base_alcohol=item_lookup,
                    drink=drink_id
                )

                return shot_recipe


class CreateDrinkRecipe(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DrinkRecipe.objects.all()
    serializer_class = DrinkRecipeSerializer


class AdminDrinkDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DrinkRecipe.objects.all()
    serializer_class = DrinkRecipeSerializer


class EditDrinkDetail(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DrinkRecipe.objects.all()
    serializer_class = DrinkRecipeSerializer


class DeleteDrinkDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DrinkRecipe.objects.all()
    serializer_class = DrinkRecipeSerializer


"""
View Classes
1. CreateAPIView - Used for create-only endpoints
2. ListAPIView - Used for read-only endpoints to represent a collection of model instances.
3. RetrieveAPIView - Used for read-only endpoints to represent a single model instance.
4. DestroyAPIView - Used for delete-only endpoints for a single model instance.
5. UpdateAPIView - used for update only endpoints for a single model instance
6. ListCreateAPIView - Used for read-write endpoints to represet a collectioni of model instance.
7. RereieveUPdateAPIView - Used for read or update endpoints to represent a single model instance.
8. RetrieveDestroyAPIView - Used for read or delete endpoints to represent a single model instance.
9. RetrieveUpdateDestroyAPIView - Used for read-wrte-delete endpoints to represent a single model instance.
"""



