
from django.contrib import admin
from django.urls import include, path
from scheduler import views

urlpatterns = [
    path('', include('scheduler.urls')),
    path('admin/', admin.site.urls),
    # Code for configuring URL of the login app adapted from Muhd Rahiman, 2/27/2021
    # https://dev.to/mdrhmn/django-google-authentication-using-django-allauth-18f8
    path('accounts/', include('allauth.urls')),
]
