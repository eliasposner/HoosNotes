from django.test import TestCase, Client
from django.contrib.auth import get_user_model
import unittest

# Create your tests here.

class LoginTest(TestCase):
	def setUp(self):
		User = get_user_model()
		user = User.objects.create_user(username='test', password='t3st!!', email='test@email.com')
		user.save()

	# Test case adapted from Professor Sherrif's lecture on 10/7/2021 at 11am
	def test_correct_credentials(self):
		c = Client()
		logged_in = c.login(username='test', password='t3st!!', email='test@email.com')
		self.assertTrue(logged_in)

	def test_incorrect_password(self):
		c = Client()
		logged_in = c.login(username='test', password='T3st!!', email='test@email.com')
		self.assertFalse(logged_in)


