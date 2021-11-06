from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from functools import reduce
from multiselectfield import MultiSelectField
import datetime


class NoteFile(models.Model):
	note = models.FileField()
	title = models.CharField(max_length=200, default='')
	upload_time = models.DateTimeField(auto_now=True)

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = "profile", null=True)

	# To retrieve the list of classes the user is enrolled in, call self.studentclass_set.all()

	def __str__(self):
		return self.user.username


#https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user = instance)
		
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

class StudentClass(models.Model):
	class_name = models.CharField(max_length=200, default='')
	instructor = models.CharField(max_length=200, default='')
	users = models.ManyToManyField(Profile)
	start_time = models.TimeField(null=True)
	end_time = models.TimeField(null=True)
	location = models.CharField(max_length=200, default='')
	enrolled_users_count = models.IntegerField(default=0)
	notes = models.ManyToManyField(NoteFile)
	DAY_OF_THE_WEEK = (
		("Sunday", "Sunday"),
		("Monday", "Monday"),
		("Tuesday", "Tuesday"),
		("Wednesday", "Wednesday"),
		("Thursday", "Thursday"),
		("Friday", "Friday"),
		("Saturday", "Saturday"),
	)

	days_of_the_week = MultiSelectField(choices = DAY_OF_THE_WEEK)


	class Meta:
		verbose_name_plural = 'Student Classes'
		unique_together = [['class_name', 'instructor']]

	def __str__(self):
		return self.class_name
	

