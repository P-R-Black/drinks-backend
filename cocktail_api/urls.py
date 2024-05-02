from django.urls import path
from .views import DrinkList, DrinkDetail, BaseDrink, MustKnows, ShotByBase, AllShots, ShotRecipe

# from .views import DrinkList
# from rest_framework.routers import DefaultRouter


app_name = 'cocktail_api'

# router = DefaultRouter()
# router.register('', DrinkList, basename='drinks')
# urlpatterns = router.urls


urlpatterns = [
    path('', DrinkList.as_view(), name="listcreate"),
    path('must-knows/', MustKnows.as_view(), name='mustknows'),
    path('<str:base_alcohol>/shot/<str:shot_name>/', ShotRecipe.as_view(), name='shotrecipe'),
    path('shots/', AllShots.as_view(), name='allshots'),
    path('<str:base_alcohol>/shot/', ShotByBase.as_view(), name='shots'),
    path('<int:pk>/', DrinkDetail.as_view(), name='detailcreate'),
    path('<str:base_alcohol>/', BaseDrink.as_view(), name='alcoholbase'),


    # path('', views.get_data),
    # path('add/', views.add_item),
]