from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)


# Create your models here.
class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, name, password=None):
        if not email:
            raise ValueError('An email address is required.')

        if not password:
            raise ValueError('A user password is required.')

        user = self.create_superuser(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return self.create_user(email, name, password)

    def create_user(self, email, name, password):
        if not email:
            raise ValueError('An email address is required.')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save()
        return user



