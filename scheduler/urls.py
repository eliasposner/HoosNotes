from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    # Code for registering the app's url from Muhd Rahiman, 2/27/2021
    # https://dev.to/mdrhmn/django-google-authentication-using-django-allauth-18f8sub
    path('', views.IndexView.as_view(), name="index_view"),

    # Code for registering the rest framework url from Moeedlodhi, 6/21/2021
    # https://medium.com/geekculture/getting-started-with-django-social-authentication-80ee7dc26fe0
    path('rest-auth/google/', views.GoogleLogin.as_view(), name='redirect'),
    
    path('createclass', views.StudentClassCreateView.as_view(), name='create_student_class'),
    path('listclasses/', views.StudentClassListView.as_view(), name = 'list_student_classes'),
    path('joinclasses/', views.StudentClassJoinView.as_view(), name = 'join_student_classes'),
    path('class/<int:pk>/', views.ClassView.as_view(), name="class_detail"),
]
