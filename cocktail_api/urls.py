from django.urls import path
from .views import DrinkList, DrinkDetail

app_name = 'cocktail_api'

urlpatterns = [
    path('<int:pk>/', DrinkDetail.as_view(), name='detailcreate'),
    path('', DrinkList.as_view(), name="listcreate"),
    # path('', views.get_data),
    # path('add/', views.add_item),
]