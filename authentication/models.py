import uuid

import jwt
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework import authentication, exceptions
from rest_framework.authentication import get_authorization_header

from teddy import settings


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username, firstname, lastname, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
        return self.create_superuser(email, username, firstname, lastname, password, **other_fields)

    def create_user(self, email, username, firstname, lastname, password, **other_fields):
        if not email:
            raise ValueError(_('Email address is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=firstname, last_name=lastname, **other_fields)
        user.set_password(password)
        user.save()
        return user


class Account(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$', message="Phone number must be entered in the format: '+84123456789'. Up to 12 characters allowed.")
    phone = models.CharField(blank=True, max_length=12, validators=[phone_regex])

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.username


# class JWTAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request): # it will return user object
#         try:
#             token = get_authorization_header(request).decode('utf-8')
#             if token is None or token == "null" or token.strip() == "":
#                 raise exceptions.AuthenticationFailed('Authorization Header or Token is missing on Request Headers')
#             print(token)
#             decoded = jwt.decode(token, settings.SECRET_KEY)
#             username = decoded['username']
#             user_obj = Account.objects.get(username=username)
#         except jwt.ExpiredSignature :
#             raise exceptions.AuthenticationFailed('Token Expired, Please Login')
#         except jwt.DecodeError :
#             raise exceptions.AuthenticationFailed('Token Modified by thirdparty')
#         except jwt.InvalidTokenError:
#             raise exceptions.AuthenticationFailed('Invalid Token')
#         except Exception as e:
#             raise exceptions.AuthenticationFailed(e)
#         return (user_obj, None)
#
#     def get_user(self, userid):
#         try:
#             return Account.objects.get(id=userid)
#         except Exception as e:
#             return None