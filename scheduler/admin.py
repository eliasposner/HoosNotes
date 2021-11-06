from django.contrib import admin
from .models import Profile, StudentClass, NoteFile

# Register your models here.
admin.site.register(Profile)
admin.site.register(StudentClass)
admin.site.register(NoteFile)