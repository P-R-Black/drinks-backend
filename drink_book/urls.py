"""drink_book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
import environ
import os
import debug_toolbar

env = environ.Env()
environ.Env.read_env()

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(env('SECRET_ADMIN_URL') + '/admin/', admin.site.urls),
    path('', include('base.urls', namespace='base')),
    path('api/', include('cocktail_api.urls',  namespace='cocktail_api')),  # 'cocktail_api.urls',
    path('api/user/', include('accounts.urls', namespace='accounts')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('__debug__/', include(debug_toolbar.urls)),
   ]
