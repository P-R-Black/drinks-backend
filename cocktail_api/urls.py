from django.urls import path
from .views import (DrinkListV1, DrinkDetailV1, BaseDrinkV1, AllCocktailsV1, AllCocktailsByBaseV1, MustKnowsV1,
                    ShotByBaseV1, AllShotsV1, CreateDrinkRecipe, AdminDrinkDetail, EditDrinkDetail,
                    DeleteDrinkDetail, MostPopularV1, MostPopularByBaseV1, AlcoholTypeListViewV1,
                    ShotAlcoholTypeListViewV1, CocktailAlcoholTypeListViewV1)

# from .views import DrinkList
# from rest_framework.routers import DefaultRouter


app_name = 'cocktail_api'

# router = DefaultRouter()
# router.register('', DrinkList, basename='drinks')
# urlpatterns = router.urls


urlpatterns = [
    path('v1/all-alcohol-types', AlcoholTypeListViewV1.as_view(), name='alcohol-type-list'),
    path('v1/cocktail-alcohol-types', CocktailAlcoholTypeListViewV1.as_view(), name='cocktail-alcohol-type-list'),
    path('v1/shot-alcohol-types', ShotAlcoholTypeListViewV1.as_view(), name='shot-alcohol-type-list'),
    path('v1/drinks', DrinkListV1.as_view(), name="listcreate"),
    path('v1/cocktails', AllCocktailsV1.as_view(), name='cocktails'),
    path('v1/cocktail/<str:base_alcohol>', AllCocktailsByBaseV1.as_view(), name='cocktais-by-base'),
    path('v1/must-knows', MustKnowsV1.as_view(), name='mustknows'),
    path('v1/most-popular', MostPopularV1.as_view(), name='mostpopular'),
    path('v1/most-popular/<str:base_alcohol>', MostPopularByBaseV1.as_view(), name='mostpopularbybase'),
    path('v1/shot', AllShotsV1.as_view(), name='allshots'),
    path('v1/shot/<str:base_alcohol>', ShotByBaseV1.as_view(), name='shots'),
    path('v1/<int:pk>', DrinkDetailV1.as_view(), name='detailcreate'),
    path('v1/<str:base_alcohol>', BaseDrinkV1.as_view(), name='alcoholbase'),
    # Drink Admin URLS
    path('admin/create', CreateDrinkRecipe.as_view(), name='createdrinkrecipe'),
    path('admin/edit/drinkdetail/<int:pk>', AdminDrinkDetail.as_view(), name='admindetaildrink'),
    path('admin/edit/<int:pk>', EditDrinkDetail.as_view(), name='editdrink'),
    path('admin/delete/<int:pk>', DeleteDrinkDetail.as_view(), name='deletederink')
]