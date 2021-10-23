from django.contrib import admin
from django.urls import path, include
from . import views

# Code for registering the app's url from Muhd Rahiman, 2/27/2021
# https://dev.to/mdrhmn/django-google-authentication-using-django-allauth-18f8
urlpatterns = [
    path('', views.view_name, name="view_name"),
    path('classes/', views.ClassListView.as_view(), name = 'Classes'),
    path('create/', views.ClassView, name = 'ClassCreate'),
]