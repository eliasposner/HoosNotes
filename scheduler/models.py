from django.db import models

# Create your models here.
<<<<<<< HEAD
<<<<<<< HEAD
=======

class Class(models.Model):
    """user = models.ForeignKey(User, on_delete=models.CASCADE)"""
    classname = models.CharField(max_length=200)
    def __str__(self):
        return self.classname
>>>>>>> parent of 548273d (Adding user specific data access)
=======
>>>>>>> parent of af0b7a3 (Start of first major feature)
