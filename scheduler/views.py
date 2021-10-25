from django.shortcuts import render
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from scheduler.models import StudentClass
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

class IndexView(TemplateView):
    template_name = 'scheduler/index.html'

# Code for returning a token given the Google Access code from Moeedlodhi, 6/21/2021
# https://medium.com/geekculture/getting-started-with-django-social-authentication-80ee7dc26fe0
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

def post(self, request, *args, **kwargs):
        response = super(GoogleLogin, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['key'])
        return Response({'token': token.key, 'id': token.user_id})


class StudentClassCreateView(CreateView):
    model = StudentClass
    fields = ['class_name', 'instructor']
    template_name = 'scheduler/createclass.html'
    success_url = '../'


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

