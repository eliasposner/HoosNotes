from django.contrib.auth.models import User
from django.db.models.fields import GenericIPAddressField
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from scheduler.models import StudentClass, Profile, NoteFile, TodoListItem
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views import generic
from django.views.generic.list import ListView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse

# Code for returning a token given the Google Access code from Moeedlodhi, 6/21/2021
# https://medium.com/geekculture/getting-started-with-django-social-authentication-80ee7dc26fe0
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

def post(self, request, *args, **kwargs):
        response = super(GoogleLogin, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['key'])
        return Response({'token': token.key, 'id': token.user_id})

# todoappView, a function based view for displaying TodoListItems the user has created
# Adapted from Ashwin Joy
# URL: https://pythonistaplanet.com/to-do-list-app-using-django/
def todoappView(request):
    if request.user.is_anonymous:
        return render(request, 'scheduler/index.html')
    q1 = Profile.objects.filter(user=request.user)[0]
    user_todo_items = q1.todolistitem_set.all()
    return render(request, 'scheduler/index.html', {'all_items':user_todo_items}) 


# addTodoView, a function based view for adding TodoListItems
# Adapted from Ashwin Joy
# URL: https://pythonistaplanet.com/to-do-list-app-using-django/
def addTodoView(request):
    new_item = TodoListItem(content = request.POST['content'])
    new_item.save()
    new_item.users.add(request.user.profile)
    new_item.save()
    return HttpResponseRedirect('/') 


# deleteTodoView, a function based view for deleting TodoListItems
# Adapted from Ashwin Joy 
# URL: https://pythonistaplanet.com/to-do-list-app-using-django/
def deleteTodoView(request, i):
    todo_item = TodoListItem.objects.get(id=i)
    todo_item.delete()
    return HttpResponseRedirect('/') 

# https://stackoverflow.com/questions/46378465/class-based-views-cbv-createview-and-request-user-with-a-many-to-many-relatio
@method_decorator(login_required(login_url='/accounts/google/login'), name='dispatch')
class StudentClassCreateView(CreateView):
    model = StudentClass
    fields = ['class_name', 'instructor', 'start_time', 'end_time', 'location', 'days_of_the_week']
    template_name = 'scheduler/createclass.html'
    success_url = '/listclasses'
    def form_valid(self, form):
        self.object = form.save()
        self.object.users.add(self.request.user.profile)
        self.object.enrolled_users_count += 1
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required(login_url='/accounts/google/login'), name='dispatch')

class StudentClassJoinView(CreateView):
    model = StudentClass
    fields = ['class_name', 'instructor', 'start_time', 'end_time', 'location', 'days_of_the_week']
    template_name = 'scheduler/joinclass.html'
    success_url = '/joinclasses'
    def form_valid(self, form):
        self.object = form.save()
        self.object.users.add(self.request.user.profile)
        self.object.enrolled_users_count += 1
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required(login_url='/accounts/google/login'), name='dispatch')

class StudentClassListView(ListView):
    model = Profile
    template_name = 'scheduler/listclass.html'
    context_object_name = 'list_of_classes'
    def get_queryset(self):
        q1 = Profile.objects.filter(user=self.request.user)[0]
        return q1.studentclass_set.all()#Profile.objects.filter(user=self.request.user)

@method_decorator(login_required(login_url='/accounts/google/login'), name='dispatch')
class ClassView(DetailView):
    model = StudentClass
    template_name = 'scheduler/class.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = self.object.notes.filter(user = self.request.user.profile)
        return context


def AddNote(request, pk):
    studentclass = get_object_or_404(StudentClass, pk=pk)
    note = NoteFile(note = request.FILES['noteFile'], title = request.POST['title'])
    if note.title == '':
        note.title = note.note.name
    note.save()
    note.user.set([request.user.profile])
    note.save()
    studentclass.notes.add(note)
    studentclass.save()
    return HttpResponseRedirect(reverse('class_detail', args=(studentclass.id,)))

'''
def classpage(request, class_id):
    desiredClass = get_object_or_404(StudentClass, pk=class_id)
    return HttpResponseRedirect(reverse('scheduler:class', args = (desiredClass.id,)))
'''

# Code for logout functionality. Deletes both the regular token and social token (if it exists) when the user sends a logout request
# Adapted from Moeedlodhi, 6/21/2021
# https://medium.com/geekculture/getting-started-with-django-social-authentication-80ee7dc26fe0
@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def User_logout(request):
    try:
        access_token = SocialToken.objects.filter(account__user=request.user, account__provider='google')
        social_token=[items.delete() for items in access_token]
    except:
        pass
    request.user.auth_token.delete()

    logout(request)

    return Response('User Logged out successfully')

