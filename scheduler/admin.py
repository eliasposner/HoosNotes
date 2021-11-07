from django.contrib import admin
from .models import Profile, StudentClass, NoteFile, TodoListItem

# Register your models here.
admin.site.register(Profile)
admin.site.register(StudentClass)
admin.site.register(NoteFile)
admin.site.register(TodoListItem)