from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=40)
	
class StudentClass(models.Model):
	class_name = models.CharField(max_length=200, default ='')
	instructor = models.CharField(max_length=200, default='')
	enrolled_users = models.JSONField(default=[])
	enrolled_users_count = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = 'Student Classes'

	def __str__(self):
		return self.class_name

