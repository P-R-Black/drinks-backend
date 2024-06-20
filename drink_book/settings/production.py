from .base import *

ALLOWED_HOSTS = ['keepsguide.paulrblack.com', 'www.keepsguide.paulrblack.com', '162.243.168.128']

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env('DRINKBOOK_DB_ENGINE'),
        'NAME': env('DRINKBOOK_DB_NAME'),
        'USER': env('DRINKBOOK_DB_USER'),
        'PASSWORD': env('DRINKBOOK_DB_PASSWORD'),
        'HOST': env('DRINKBOOK_DB_HOST'),
        'PORT': env('DRINKBOOK_DB_PORT')
    }
}


