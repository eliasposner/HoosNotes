from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    # Code for registering the app's url from Muhd Rahiman, 2/27/2021
    # https://dev.to/mdrhmn/django-google-authentication-using-django-allauth-18f8
    path('', views.view_name, name="view_name"),

    # Code for registering the rest framework url from Moeedlodhi, 6/21/2021
    # https://medium.com/geekculture/getting-started-with-django-social-authentication-80ee7dc26fe0
    path('rest-auth/google/', views.GoogleLogin.as_view(), name='redirect')
]