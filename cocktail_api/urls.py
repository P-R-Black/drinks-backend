from django.urls import path
from .views import DrinkList, DrinkDetail, BaseDrink, MustKnows

# from .views import DrinkList
# from rest_framework.routers import DefaultRouter


app_name = 'cocktail_api'

# router = DefaultRouter()
# router.register('', DrinkList, basename='drinks')
# urlpatterns = router.urls


urlpatterns = [
    path('', DrinkList.as_view(), name="listcreate"),
    path('must-knows/', MustKnows.as_view(), name='mustknows'),
    path('<int:pk>/', DrinkDetail.as_view(), name='detailcreate'),
    path('<str:drink>/', BaseDrink.as_view(), name='alcoholbase'),


    # path('', views.get_data),
    # path('add/', views.add_item),
]