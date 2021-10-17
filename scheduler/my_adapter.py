'''
my_adapter.py
This file handles email collisions (when a social account and a regular account have the same email).
The Google account will be linked to the regular account to preven the same email from being twice.

Code is copied from Moeedlodhi, 6/21/2021
https://medium.com/geekculture/getting-started-with-django-social-authentication-80ee7dc26fe0
'''

from django.contrib.auth import get_user_model
User = get_user_model()
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from rest_framework.response import Response


class MyAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # This isn't tested, but should work
        if sociallogin.is_existing:
            return

            # some social logins don't have an email address, e.g. facebook accounts
            # with mobile numbers only, but allauth takes care of this case so just
            # ignore it
        if 'email' not in sociallogin.account.extra_data:
            return
        try:
            user = User.objects.get(email=sociallogin.user.email)
            sociallogin.connect(request, user)
            # Create a response object
            raise ImmediateHttpResponse('hello')
        except User.DoesNotExist:
            pass