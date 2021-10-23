from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from scheduler.models import Class
from .forms import ClassForm
from django.views import generic



# https://dev.to/mdrhmn/django-google-authentication-using-django-allauth-18f8
def view_name(request):
    return render(request, 'scheduler/index.html', {})



""" In ClassView you should be able to create a class and s
    this should redirect you to the list of classes so that
    you can join them."""

def ClassView(request):
    template_name = 'scheduler/class.html'
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
    form = ClassForm()
    return render(request, "scheduler/class.html", {'form': form})

""" In ClassListView the list of classes should be shown
    and in the template you should be able to select a 
    a class or create one. If you press create it should 
    redirect to ClassView template which is where you fill
    out a form and create a class."""

class ClassListView(generic.ListView):
    models = Class
    template_name = 'scheduler/classlist.html'
    context_object_name = 'list_of_classes'
    def get_queryset(self):
        return Class.object.all()
