from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
import unittest

# Create your tests here.
class SignUpTest(TestCase):

	def test_create_account_with_password(self):
		User = get_user_model()
		alice = User.objects.create_user(username='alice', password='inw0nd3rland', email='alice@gmail.com')
		allUsers = User.objects.all()
		self.assertTrue(alice in allUsers)

	def test_create_account_without_password(self):
		User = get_user_model()
		bob = User.objects.create_user(username='bob', email='bob@gmail.com')
		allUsers = User.objects.all()
		self.assertTrue(bob in allUsers)

	def test_create_account_no_credentials(self):
		User = get_user_model()
		self.assertRaises(TypeError, User.objects.create_user)

	def test_create_account_empty_credentials(self):
		User = get_user_model()
		self.assertRaises(ValueError, User.objects.create_user, username='', password='', email='')


class LoginTest(TestCase):

	def setUp(self):
		User = get_user_model()
		user = User.objects.create_user(username='correctUser', password='c0rrectpassw0rd', email='correctUser@email.com')

	def test_login_correct_credentials(self):	
		logged_in = self.client.login(username='correctUser', password='c0rrectpassw0rd')
		self.assertTrue(logged_in)

	def test_login_incorrect_password(self):
		logged_in = self.client.login(username='correctUser', password='inc0rrectpassw0rd')
		self.assertFalse(logged_in)

	def test_login_incorrect_user(self):
		logged_in = self.client.login(username='incorrectUser', password='c0rrectpassw0rd')
		self.assertFalse(logged_in)

	def test_login_incorrect_credentials(self):
		logged_in = self.client.login(username='incorrectUser', password='inc0rrectpassw0rd')

	def test_login_no_credentials(self):
		logged_in = self.client.login()
		self.assertFalse(logged_in)

	def test_sql_injection(self):
		logged_in = self.client.login(username='\' or 1=1 #', password='', email='')
		self.assertFalse(logged_in)


class LogoutTest(TestCase):
	def setUp(self):
		User = get_user_model()
		self.testUser = User.objects.create_user(username='testUser', password='t3stpassw0rd', email='testUser@email.com')
		self.client.login(username='testUser', password='t3stpassw0rd')

	def test_logout_redirect(self):
		# Logout test case adapted from Astik Anand, 7/16/19
		# https://stackoverflow.com/questions/57048654/how-to-assert-the-user-is-logout-in-django-test-testcase
		# Description: makes sure the logout url permanently redirects user
		request = self.client.get('/accounts/logout/')
		self.assertEquals(request.status_code, 302)

class CreateClassTest(TestCase):

	def setUp(self):
		User = get_user_model()
		testUser = User.objects.create_user(username='testUser', password='t3stpassw0rd', email='testUser@email.com')

	def test_redirect_when_not_logged_in(self):
		request = self.client.get('/createclass')
		self.assertEquals(request.status_code, 302)

	def test_access_when_logged_in(self):
		self.client.login(username='testUser', password='t3stpassw0rd')
		request = self.client.get('/createclass')
		self.assertEquals(request.status_code, 200)

