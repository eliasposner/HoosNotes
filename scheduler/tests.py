from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import unittest

# Create your tests here.

class LoginTest(unittest.TestCase):
	
	#def setUp(self):
	#	User = get_user_model()
		#user = User.objects.create_user(username='test', email='test@email.com')
		#user.save()

		#allUsers = User.objects.all()


	# Check if registered account exists
	def test_registered_acc_exists(self):
		User = get_user_model()
		user = User.objects.get(username='keith')
		allUsers = User.objects.all()
		self.assertTrue(user in allUsers)

	def test_unregistered_acc_does_not_exist(self):
		User = get_user_model()
		allUsers = User.objects.all()
		unregisted_user = User(username='unregistered', email='unregistered@email.com')
		self.assertFalse(unregisted_user in allUsers)

	def test_account_is_created(self):
		User = get_user_model()
		user = User.objects.create_user(username='newUser', email='newUser@email.com')
		allUsers = User.objects.all()
		self.assertTrue(user in allUsers)

	# Check if unregistered account does not exist
	#def test_unregistered_acc_does_not_exist(self):


