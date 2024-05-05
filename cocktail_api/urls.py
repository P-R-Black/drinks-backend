from django.urls import path
from .views import (DrinkList, DrinkDetail, BaseDrink, AllCocktails, MustKnows, ShotByBase, AllShots, ShotRecipe,
                    CreateDrinkRecipe, AdminDrinkDetail, EditDrinkDetail, DeleteDrinkDetail, MostPopular)

# from .views import DrinkList
# from rest_framework.routers import DefaultRouter


app_name = 'cocktail_api'

# router = DefaultRouter()
# router.register('', DrinkList, basename='drinks')
# urlpatterns = router.urls


urlpatterns = [
    path('', DrinkList.as_view(), name="listcreate"),
    path('cocktails/', AllCocktails.as_view(), name='coctails'),
    path('must-knows/', MustKnows.as_view(), name='mustknows'),
    path('most-popular/', MostPopular.as_view(), name='mostpopular'),
    path('<str:base_alcohol>/shot/<str:shot_name>/', ShotRecipe.as_view(), name='shotrecipe'),
    path('shot/', AllShots.as_view(), name='allshots'),
    path('<str:base_alcohol>/shot/', ShotByBase.as_view(), name='shots'),
    path('<int:pk>/', DrinkDetail.as_view(), name='detailcreate'),
    path('<str:base_alcohol>/', BaseDrink.as_view(), name='alcoholbase'),
    # Drink Admin URLS
    path('admin/create/', CreateDrinkRecipe.as_view(), name='createdrinkrecipe'),
    path('admin/edit/drinkdetail/<int:pk>/', AdminDrinkDetail.as_view(), name='admindetaildrink'),
    path('admin/edit/<int:pk>/', EditDrinkDetail.as_view(), name='editdrink'),
    path('admin/delete/<int:pk>', DeleteDrinkDetail.as_view(), name='deletederink')
]