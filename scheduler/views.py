<<<<<<< HEAD
from django.shortcuts import render
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
=======
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from scheduler.models import Class
from .forms import ClassForm
from django.views import generic

>>>>>>> romanBranch2

# Code for rendering the login success template from Mudh Rahiman, 2/27/2021
# https://dev.to/mdrhmn/django-google-authentication-using-django-allauth-18f8
def view_name(request):
    return render(request, 'scheduler/index.html', {})

<<<<<<< HEAD
# Code for returning a token given the Google Access code from Moeedlodhi, 6/21/2021
# https://medium.com/geekculture/getting-started-with-django-social-authentication-80ee7dc26fe0
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

def post(self, request, *args, **kwargs):
        response = super(GoogleLogin, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['key'])
        return Response({'token': token.key, 'id': token.user_id})


# Code for logout functionality. Deletes both the regular token and social token (if it exists) when the user sends a logout request
# Adapted from Moeedlodhi, 6/21/2021
# https://medium.com/geekculture/getting-started-with-django-social-authentication-80ee7dc26fe0
@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def User_logout(request):
    try:
        access_token = SocialToken.objects.filter(account__user=request.user, account__provider='google')
        social_token=[items.delete() for items in access_token]
    except:
        pass
    request.user.auth_token.delete()

    logout(request)

    return Response('User Logged out successfully')
=======


""" In ClassView you should be able to create a class and s
    this should redirect you to the list of classes so that
    you can join them."""

def ClassView(request):
    template_name = 'scheduler/class.html'
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
    form = ClassForm()
    return render(request, "scheduler/class.html", {'form': form})

""" In ClassListView the list of classes should be shown
    and in the template you should be able to select a 
    a class or create one. If you press create it should 
    redirect to ClassView template which is where you fill
    out a form and create a class."""

class ClassListView(generic.ListView):
    models = Class
    template_name = 'scheduler/classlist.html'
    context_object_name = 'list_of_classes'
    def get_queryset(self):
        return Class.object.all()

def lists_classes(request):
    classes = Class.objects.all().filter(user=request.user)
    
>>>>>>> romanBranch2
