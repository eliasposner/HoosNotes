from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
import unittest

# Create your tests here.

class LoginTest(TestCase):

	def test_unregistered_acc_does_not_exist(self):
		User = get_user_model()
		allUsers = User.objects.all()
		unregisted_user = User(username='unregistered', email='unregistered@email.com')
		self.assertFalse(unregisted_user in allUsers)
	

	def test_create_account(self):
		User = get_user_model()
		user = User.objects.create_user(username='newUser', email='newUser@email.com')
		allUsers = User.objects.all()
		self.assertTrue(user in allUsers)




