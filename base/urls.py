from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'base'

urlpatterns = [
    # path('', TemplateView.as_view(template_name="home/home.html")),
    path('docs/', views.docs_page, name='docs_page'),
    path('about/', views.about_page, name='about_page'),
    path('', views.home_page, name='home_page'),


]