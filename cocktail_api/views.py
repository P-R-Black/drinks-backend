from rest_framework.permissions import (
    SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission,
    IsAdminUser, DjangoModelPermissionsOrAnonReadOnly, AllowAny)
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from rest_framework import generics
from django.conf import settings
from base.models import Drink, DrinkRecipe, AlcoholType
from .serializers import DrinkRecipeSerializerV1, AlcoholTypeSerializerV1
from django.utils.text import slugify
import redis
import logging
from .mixins import MetadataMixin
from django.http import JsonResponse

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

logger = logging.getLogger(__name__)
logging.basicConfig(filename='cocktail_api.log', level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


class UserWritePermission(BasePermission):
    message = "Editing Drink Data is Restriced to Admin Only"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user


class DrinkListV1(MetadataMixin, generics.ListAPIView):
    permission_classes = [HasAPIKey]  #[AllowAny]
    queryset = DrinkRecipe.objects.all()
    serializer_class = DrinkRecipeSerializerV1
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        # cache.clear()
        cache_key = 'drink_list'
        cache_time = 86400
        queryset = cache.get(cache_key)
        logger.debug(f'DrinkList/drink_list from cache. Cache hit!!')

        if not queryset:
            logger.debug(f'Cache miss for DrinkList/drink_list data_queryset: fetching data_queryset from database')
            queryset = super().get_queryset()
            cache.set(cache_key, queryset, cache_time)

        logger.debug(f'Returning queryset cocktail_api/drink_list: {queryset}')

        # Serialize the data
        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data

        metadata = self.get_metadata(serialized_data)
        return Response(metadata)


class DrinkDetailV1(MetadataMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [HasAPIKey]  # [UserWritePermission]
    serializer_class = DrinkRecipeSerializerV1
    queryset = DrinkRecipe.objects.all()

    def retrieve(self, request, *args, **kwargs):
        # Get the drink recipe ID from the URL kwargs
        drink_id = self.kwargs.get('pk')
        cache_key = f'drink_detail_{drink_id}'
        cache_time = 86400  # Cache for 24 hours

        # Try to get the drink recipe data from the cache
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.debug(f'DrinkDetailV1/retrieve: cache hit for {cache_key}')
            return Response(cached_data)

        # Cache miss, fetch the data from the database
        logger.debug(f'DrinkDetailV1/retrieve: cache miss for {cache_key}, fetching data from DB')
        response = super().retrieve(request, *args, **kwargs)

        # Prepare the metadata using the mixin and serialized data
        serialized_data = response.data
        metadata = self.get_metadata(serialized_data)

        # Cache the metadata and serialized data
        cache.set(cache_key, metadata, cache_time)
        logger.debug(f'DrinkDetailV1/retrieve: data cached for {cache_key}')

        # Return the response with metadata
        return Response(metadata)

    def update(self, request, *args, **kwargs):
        # Invalidate the cache when the object is updated
        drink_id = self.kwargs.get('pk')
        cache_key = f'drink_detail_{drink_id}'
        cache.delete(cache_key)  # Clear the cache when updating
        logger.debug(f'DrinkDetailV1/update: cache invalidated for {cache_key}')

        # Perform the update as usual
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Invalidate the cache when the object is deleted
        drink_id = self.kwargs.get('pk')
        cache_key = f'drink_detail_{drink_id}'
        cache.delete(cache_key)  # Clear the cache when deleting
        logger.debug(f'DrinkDetailV1/destroy: cache invalidated for {cache_key}')

        # Perform the deletion as usual
        return super().destroy(request, *args, **kwargs)


class AllCocktailsV1(MetadataMixin, generics.ListCreateAPIView):
    permission_classes = [HasAPIKey] # [AllowAny]
    serializer_class = DrinkRecipeSerializerV1
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # Filter for only cocktails
        return DrinkRecipe.objects.filter(drink_type="cocktail")

    def list(self, request, *args, **kwargs):
        cache_key = 'cocktail_list'
        cache_time = 86400  # Cache for 24 hours

        # Try to get the data from cache
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.debug(f'AllCocktailsV1/list: cache hit for {cache_key}')
            return Response(cached_data)

        # Cache miss, fetch the data from the database
        logger.debug(f'AllCocktailsV1/list: cache miss for {cache_key}, fetching data from DB')
        queryset = self.get_queryset()

        # Serialize the data
        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data

        # Prepare the metadata using the mixin
        metadata = self.get_metadata(serialized_data)

        # Cache the metadata and serialized data
        cache.set(cache_key, metadata, cache_time)
        logger.debug(f'AllCocktailsV1/list: data cached for {cache_key}')

        # Return the response with metadata
        return Response(metadata)


class AllCocktailsByBaseV1(MetadataMixin, generics.ListCreateAPIView):
    permission_classes = [HasAPIKey] # [AllowAny]
    serializer_class = DrinkRecipeSerializerV1
    pagination_class = PageNumberPagination

    def get_queryset(self, **kwargs):
        base = slugify(self.kwargs.get('base_alcohol'))

        # Generate a unique cache key based on the base alcohol type
        cache.clear()
        cache_key = f'cocktails_by_base_{base}'
        cache_time = 86400  # Cache time for 24 hours

        # Check if the queryset is cached
        queryset = cache.get(cache_key)
        if queryset:
            logger.debug(f'ShotByBaseV1/get_queryset: cache hit for {cache_key}')
            return queryset

        # If not cached, fetch the data
        base_alc_two = AlcoholType.objects.all()
        for item in base_alc_two.values():
            if slugify(item['name']) == base:
                item_lookup = item['id']
                queryset = DrinkRecipe.objects.filter(drink_type='cocktail', base_alcohol=item_lookup)

                # Cache the result
                cache.set(cache_key, queryset, cache_time)
                logger.debug(f'ShotByBaseV1/get_queryset: data cached for {cache_key}')
                return queryset

        # Return an empty queryset if no match is found
        return DrinkRecipe.objects.none()

    def list(self, request, *args, **kwargs):
        # Fetch the queryset (from cache or DB)
        queryset = self.get_queryset()

        # Serialize the data
        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data

        # Paginate the data
        page = self.paginate_queryset(queryset)
        if page is not None:
            paginated_data = self.get_paginated_response(serializer.data)

            # Add metadata to paginated data
            metadata = self.get_metadata(paginated_data.data)
            return Response(metadata)

        # If no pagination, return serialized data with metadata
        metadata = self.get_metadata(serialized_data)
        return Response(metadata)


class BaseDrinkV1(MetadataMixin, generics.ListCreateAPIView):
    permission_classes = [HasAPIKey] # [AllowAny]
    serializer_class = DrinkRecipeSerializerV1
    pagination_class = PageNumberPagination

    def get_queryset(self, **kwargs):
        base = slugify(self.kwargs.get('base_alcohol'))
        base_alc_two = AlcoholType.objects.all()
        for item in base_alc_two.values():
            if slugify(item['name']) == base:
                item_lookup = item['id']
                return DrinkRecipe.objects.filter(base_alcohol=item_lookup)

        return DrinkRecipe.objects.all()

    def list(self, request, *args, **kwargs):
        # Fetch the queryset using the get_queryset method
        base_alcohol = self.kwargs.get('base_alcohol')
        cache_key = f'drink_list_{slugify(base_alcohol)}'
        cache_time = 86400

        cached_data = cache.get(cache_key)
        if cached_data:
            logger.debug(f'BaseDrink/list: cache heit for {cache_key}')
            return Response(cached_data)

        logger.debug(f'BaseDrink/list: cache miss for {cache_key}, fetching data from DB')
        queryset = self.get_queryset()

        # Serialize the data
        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data

        # Prepare the metadata using the mixin
        metadata = self.get_metadata(serialized_data)

        cache.set(cache_key, metadata, cache_time)
        logger.debug(f'BaseDrink/list: data cached for {cache_key}')

        # Return the Response with metadata and serialized drinks
        return Response(metadata)


class MustKnowsV1(MetadataMixin, generics.ListCreateAPIView):
    permission_classes = [HasAPIKey] # [AllowAny]
    serializer_class = DrinkRecipeSerializerV1
    pagination_class = PageNumberPagination

    def get_queryset(self):
        must_knows = DrinkRecipe.objects.filter(must_know_drink=True)
        return must_knows

    def list(self, request, *args, **kwargs):
        # Fetch the queryset using the get_queryset method
        queryset = self.get_queryset()

        # Serialize the data
        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data

        # Prepare the metadata using the mixin
        metadata = self.get_metadata(serialized_data)

        # Return the Response with metadata and serialized drinks
        return Response(metadata)


class MostPopularV1(MetadataMixin, generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = DrinkRecipeSerializerV1
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # Define the cache key and time
        cache_key = 'most_popular'
        cache_time = 86400  # Cache for 24 hours

        # Check if the queryset is in the cache
        queryset = cache.get(cache_key)
        if queryset:
            logger.debug(f'MostPopularV1/get_queryset: cache hit for {cache_key}')
        else:
            # Cache miss, query the database
            logger.debug(f'MostPopularV1/get_queryset: cache miss for {cache_key}, fetching data from DB')
            queryset = DrinkRecipe.objects.filter(top_hundred_drink=True)
            cache.set(cache_key, queryset, cache_time)
            logger.debug(f'MostPopularV1/get_queryset: data cached for {cache_key}')
        return queryset

    def list(self, request, *args, **kwargs):
        # Get the cached or fetched queryset
        queryset = self.get_queryset()

        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data)

            # Prepare metadata and return paginated response
            metadata = self.get_metadata(paginated_data.data)
            return Response(metadata)

        # If not paginated, serialize the data and prepare metadata
        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data
        metadata = self.get_metadata(serialized_data)
        return Response(metadata)


class MostPopularByBaseV1(MetadataMixin, generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = DrinkRecipeSerializerV1
    pagination_class = PageNumberPagination

    def get_queryset(self, **kwargs):
        # Slugify the base alcohol type from the URL
        base = slugify(self.kwargs.get('base_alcohol'))

        # Cache key based on the base alcohol to uniquely store/filter results
        cache_key = f'most_popular_by_base_{base}'
        cache_time = 86400  # Cache for 24 hours

        # Check cache for the result
        queryset = cache.get(cache_key)
        if queryset:
            logger.debug(f'MostPopularByBaseV1/get_queryset: cache hit for {cache_key}')
            return queryset

        # If not in cache, fetch the alcohol type and query the database
        logger.debug(f'MostPopularByBaseV1/get_queryset: cache miss for {cache_key}')
        base_alcohol = AlcoholType.objects.all()
        for item in base_alcohol.values():
            if slugify(item['name']) == base:
                item_lookup = item['id']
                queryset = DrinkRecipe.objects.filter(top_hundred_drink=True, base_alcohol=item_lookup)

                # Cache the queryset
                cache.set(cache_key, queryset, cache_time)
                logger.debug(f'MostPopularByBaseV1/get_queryset: data cached for {cache_key}')
                return queryset

        # Return an empty queryset if no matching base alcohol found
        return DrinkRecipe.objects.none()

    def list(self, request, *args, **kwargs):
        # Get the cached or fetched queryset
        queryset = self.get_queryset()

        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data)

            # Prepare metadata and return paginated response
            metadata = self.get_metadata(paginated_data.data)
            return Response(metadata)

        # If not paginated, serialize the data and prepare metadata
        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data
        metadata = self.get_metadata(serialized_data)
        return Response(metadata)


class AllShotsV1(MetadataMixin, generics.ListAPIView):
    permission_classes = [HasAPIKey] # [AllowAny]
    serializer_class = DrinkRecipeSerializerV1
    pagination_class = PageNumberPagination

    def get_queryset(self):
        cache_key = 'all_shots'
        cache_time = 86400  # Cache for 24 hours

        # Check if the queryset is cached
        queryset = cache.get(cache_key)
        if queryset:
            logger.debug(f'AllShots/get_queryset: cache hit for {cache_key}')
            return queryset

        # If not cached, fetch the data
        queryset = DrinkRecipe.objects.filter(drink_type="shot")

        # Cache the queryset
        cache.set(cache_key, queryset, cache_time)
        logger.debug(f'AllShots/get_queryset: data cached for {cache_key}')
        return queryset

    def list(self, request, *args, **kwargs):
        # Fetch the queryset (from cache or DB)
        queryset = self.get_queryset()

        # Serialize the data
        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data

        # Paginate the data
        page = self.paginate_queryset(queryset)
        if page is not None:
            paginated_data = self.get_paginated_response(serializer.data)

            # Add metadata to paginated data
            metadata = self.get_metadata(paginated_data.data)
            return Response(metadata)

        # If no pagination, return serialized data with metadata
        metadata = self.get_metadata(serialized_data)
        return Response(metadata)


class ShotByBaseV1(MetadataMixin, generics.ListCreateAPIView):
    permission_classes = [HasAPIKey] #[AllowAny]
    serializer_class = DrinkRecipeSerializerV1
    pagination_class = PageNumberPagination

    def get_queryset(self, **kwargs):
        base = slugify(self.kwargs.get('base_alcohol'))

        # Generate a unique cache key based on the base alcohol type
        cache.clear()
        cache_key = f'shots_by_base_{base}'
        cache_time = 86400  # Cache time for 24 hours

        # Check if the queryset is cached
        queryset = cache.get(cache_key)
        if queryset:
            logger.debug(f'ShotByBaseV1/get_queryset: cache hit for {cache_key}')
            return queryset

        # If not cached, fetch the data
        base_alc_two = AlcoholType.objects.all()
        for item in base_alc_two.values():
            if slugify(item['name']) == base:
                item_lookup = item['id']
                queryset = DrinkRecipe.objects.filter(drink_type='shot', base_alcohol=item_lookup)

                # Cache the result
                cache.set(cache_key, queryset, cache_time)
                logger.debug(f'ShotByBaseV1/get_queryset: data cached for {cache_key}')
                return queryset

        # Return an empty queryset if no match is found
        return DrinkRecipe.objects.none()

    def list(self, request, *args, **kwargs):
        # Fetch the queryset (from cache or DB)
        queryset = self.get_queryset()

        # Serialize the data
        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data

        # Paginate the data
        page = self.paginate_queryset(queryset)
        if page is not None:
            paginated_data = self.get_paginated_response(serializer.data)

            # Add metadata to paginated data
            metadata = self.get_metadata(paginated_data.data)
            return Response(metadata)

        # If no pagination, return serialized data with metadata
        metadata = self.get_metadata(serialized_data)
        return Response(metadata)


class AlcoholTypeListViewV1(MetadataMixin, generics.ListAPIView):
    permission_classes = [HasAPIKey]  #[AllowAny]
    queryset = AlcoholType.objects.all()
    serializer_class = AlcoholTypeSerializerV1


class CocktailAlcoholTypeListViewV1(MetadataMixin, generics.ListAPIView):
    permission_classes = [HasAPIKey] # [AllowAny]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        cache_key = 'cocktail_alcohol_base_with_slug'
        cache_time = 86400  # Cache for 24 hours

        # Check if the queryset is cached
        queryset = cache.get(cache_key)
        if queryset:
            logger.debug(f'ShotAlcoholTypeListViewV1/get_queryset: cache hit for {cache_key}')
            return queryset

        # Fetch distinct base alcohol names and slugs for drinks categorized as "shots"
        queryset = (
            AlcoholType.objects
            .filter(recipes__drink_type="cocktail")  # Filter AlcoholTypes for drinks categorized as shots
            .values('name', 'slug')  # Get the name and slug of the AlcoholType
            .distinct()  # Ensure each base alcohol appears only once
        )

        # Cache the result
        cache.set(cache_key, list(queryset), cache_time)
        logger.debug(f'CocktailAlcoholTypeListViewV1/get_queryset: data cached for {cache_key}')
        return queryset

    def list(self, request, *args, **kwargs):
        # Fetch the queryset (from cache or DB)
        queryset = self.get_queryset()

        # Convert the queryset to a list if paginated
        page = self.paginate_queryset(queryset)
        if page is not None:
            paginated_data = self.get_paginated_response(page)
            return paginated_data

        # If no pagination, return as a Response
        return Response(queryset)


class ShotAlcoholTypeListViewV1(MetadataMixin, generics.ListAPIView):
    permission_classes = [HasAPIKey] # [AllowAny]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        cache_key = 'shots_alcohol_base_with_slug'
        cache_time = 86400  # Cache for 24 hours

        # Check if the queryset is cached
        queryset = cache.get(cache_key)
        if queryset:
            logger.debug(f'ShotAlcoholTypeListViewV1/get_queryset: cache hit for {cache_key}')
            return queryset

        # Fetch distinct base alcohol names and slugs for drinks categorized as "shots"
        queryset = (
            AlcoholType.objects
            .filter(recipes__drink_type="shot")  # Filter AlcoholTypes for drinks categorized as shots
            .values('name', 'slug')  # Get the name and slug of the AlcoholType
            .distinct()  # Ensure each base alcohol appears only once
        )

        # Cache the result
        cache.set(cache_key, list(queryset), cache_time)
        logger.debug(f'ShotAlcoholTypeListViewV1/get_queryset: data cached for {cache_key}')
        return queryset

    def list(self, request, *args, **kwargs):
        # Fetch the queryset (from cache or DB)
        queryset = self.get_queryset()

        # Convert the queryset to a list if paginated
        page = self.paginate_queryset(queryset)
        if page is not None:
            paginated_data = self.get_paginated_response(page)
            return paginated_data

        # If no pagination, return as a Response
        return Response(queryset)




class CreateDrinkRecipe(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DrinkRecipe.objects.all()
    serializer_class = DrinkRecipeSerializerV1


class AdminDrinkDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DrinkRecipe.objects.all()
    serializer_class = DrinkRecipeSerializerV1


class EditDrinkDetail(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DrinkRecipe.objects.all()
    serializer_class = DrinkRecipeSerializerV1


class DeleteDrinkDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DrinkRecipe.objects.all()
    serializer_class = DrinkRecipeSerializerV1


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

# class DrinkList(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = DrinkRecipeSerializerV1
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
#         serializer_class = DrinkRecipeSerializerV1(self.queryset, many=True)
#         print('serializer_class list', request)
#         return Response(serializer_class.data)
#
#     def retrieve(self, request, pk=None):
#         print('request retrieve', request)
#         drink_recipe = get_object_or_404(self.queryset, pk=pk)
#         print('drink_recipe retrieve', request)
#         serializer_class = DrinkRecipeSerializerV1(drink_recipe)
#         return Response(serializer_class.data)


# class DrinkDetailV1(MetadataMixin, generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [UserWritePermission]
#     queryset = DrinkRecipe.objects.all()
#     serializer_class = DrinkRecipeSerializerV1
#     pagination_class = PageNumberPagination

# class MostPopularByBaseV1(generics.ListCreateAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = DrinkRecipeSerializerV1
#
#     def get_queryset(self, **kwargs):
#         base = slugify(self.kwargs.get('base_alcohol'))
#         base_alcohol = AlcoholType.objects.all()
#
#         for item in base_alcohol.values():
#             if slugify(item['name']) == base:
#                 item_lookup = item['id']
#                 most_popular_by_base = DrinkRecipe.objects.filter(
#                     top_hundred_drink=True, base_alcohol=item_lookup
#                 )
#                 return most_popular_by_base

# class ShotRecipe(generics.ListCreateAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = DrinkRecipeSerializerV1
#
#     def get_queryset(self, **kwargs):
#         base = slugify(self.kwargs.get('base_alcohol'))
#         shot_name = slugify(self.kwargs.get('shot_name'))
#         drink_id = 0
#         for dro in Drink.objects.all().values():
#             if slugify(dro['drink_name']) == shot_name:
#                 drink_id = dro['id']
#                 break
#
#         base_alc_two = AlcoholType.objects.all()
#         for item in base_alc_two.values():
#             if slugify(item['spirit_type']) == base:
#                 item_lookup = item['id']
#                 shot_recipe = DrinkRecipe.objects.filter(
#                     drink_type='shot',
#                     base_alcohol=item_lookup,
#                     drink=drink_id
#                 )
#
#                 return shot_recipe

# class AllShots(generics.ListAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = DrinkRecipeSerializerV1
#     queryset = DrinkRecipe.objects.filter(drink_type="shot")
#     pagination_class = PageNumberPagination
#
#     def get_queryset(self):
#         cache_key = 'all_shots'
#         cache_time = 86400
#         queryset = cache.get(cache_key)
#
#         if not queryset:
#             queryset = super().get_queryset()
#             cache.set(cache_key, queryset, cache_time)
#
#         return queryset

# class ShotByBaseV1(generics.ListCreateAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = DrinkRecipeSerializerV1
#
#     def get_queryset(self, **kwargs):
#         base = slugify(self.kwargs.get('base_alcohol'))
#         base_alc_two = AlcoholType.objects.all()
#         for item in base_alc_two.values():
#             if slugify(item['name']) == base:
#                 item_lookup = item['id']
#                 shot_by_base = DrinkRecipe.objects.filter(drink_type='shot', base_alcohol=item_lookup)
#                 return shot_by_base