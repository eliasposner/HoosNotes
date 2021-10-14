from django.contrib import admin
from django.urls import path, include
from . import views

# https://dev.to/mdrhmn/django-google-authentication-using-django-allauth-18f8
urlpatterns = [
    path('', views.view_name, name="view_name"),
]