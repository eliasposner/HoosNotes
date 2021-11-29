from django.contrib.auth.models import User
from django.db.models.fields import GenericIPAddressField
from django.conf import settings
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from scheduler.models import StudentClass, Profile, NoteFile, TodoListItem, Event, Room
from .utils import Calendar
from .forms import EventForm, JoinForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views import generic
from django.views.generic.list import ListView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta, date
import calendar
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant

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

def joinclassView(request):
    return render(request, 'scheduler/joinclass.html')

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

# CalendarView, a view that takes all the events a user has submitted and returns it in calendar format
# Allows user to scroll between the current, previous, and next month
# Adapted from Hui Wen, 7/24/2018 and 7/29/2018
# URLs: https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html and https://www.huiwenteo.com/normal/2018/07/29/django-calendar-ii.html
class CalendarView(generic.ListView):
    model = Event
    template_name = 'scheduler/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(self.request.user.profile, d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

    def get_queryset(self):
        q1 = Profile.objects.filter(user = self.request.user)[0]
        return q1.event_set.all()
        #return Event.objects.filter(users=self.request.user.profile)


# Helper function for CalendarView that returns a datetime object of the current day
# From Hui Wen, 7/29/2018
# URL: https://www.huiwenteo.com/normal/2018/07/29/django-calendar-ii.html
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

# Helper function for CalendarView that, given a datetime object, returns the previous month
# From Hui Wen, 7/29/2018
# URL: https://www.huiwenteo.com/normal/2018/07/29/django-calendar-ii.html
def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

# Helper function for CalendarView that, given a datetime object, returns the next month
# From Hui Wen, 7/29/2018
# URL: https://www.huiwenteo.com/normal/2018/07/29/django-calendar-ii.html
def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

# event, a function based view that displays the event submission form and updates the Event model table based on user input
# code for obtaining instance, saving form, and rendering the request is adapted from Hui Wen, 7/29/2018, https://www.huiwenteo.com/normal/2018/07/29/django-calendar-ii.html
# code for deleting event is adapted from BenjaminAm, 1/11/2021, https://github.com/huiwenhw/django-calendar/issues/10
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    
    form = EventForm(request.POST or None, instance=instance)


    # Delete functionality adapted from BejaminAm, 1/11/2021
    # https://github.com/huiwenhw/django-calendar/issues/10
    
    # if user presses the save button
    if request.POST and 'save' in request.POST and form.is_valid():
        instance.save()
        instance.users.add(request.user.profile)
        instance.save()
        form.save()
        return HttpResponseRedirect(reverse('calendar'))

    # if user presses the delete button
    if request.POST and 'delete' in request.POST:
        if event_id:
            Event.objects.filter(pk=event_id).delete()
            return HttpResponseRedirect(reverse('calendar'))

    return render(request, 'scheduler/event.html', {'form': form})


@method_decorator(login_required(login_url='/accounts/google/login'), name='dispatch')
class StudentClassCreateView(CreateView):
    model = StudentClass
    fields = ['class_name', 'instructor', 'start_time', 'end_time', 'location', 'days_of_the_week']
    template_name = 'scheduler/createclass.html'
    success_url = '/listclasses'

    def clean(self):
        classes = StudentClass.objects.all()
        for c in classes:
            new = form.save(commit=False)
            if (new.class_name.strip().upper() == c.class_name.strip().upper() and new.instructor.strip().upper() == c.instructor.strip().upper() and \
                new.start_time == c.start_time and new.end_time == c.end_time):
                raise ValidationError(
            "The class you wish to add is already in the system. Please join this class through the \"Join Class\" page")
    # Form validation
    # Adapted from user zaidfazil, 9/23/2017
    # https://stackoverflow.com/questions/46378465/class-based-views-cbv-createview-and-request-user-with-a-many-to-many-relatio
    def form_valid(self, form):
        self.object = form.save()
        self.object.enrolled_users_count += 1
        self.object.users.add(self.request.user.profile)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


    # Form validation
    # Adapted from user zaidfazil, 9/23/2017
    # https://stackoverflow.com/questions/46378465/class-based-views-cbv-createview-and-request-user-with-a-many-to-many-relatio
#class StudentClassJoinView(CreateView):
    #model = StudentClass
    #fields = ['class_name', 'instructor', 'start_time', 'end_time', 'location', 'days_of_the_week']
    #template_name = 'scheduler/joinclass.html'
    #success_url = '/joinclasses'
    #def form_valid(self, form):
        #self.object = form.save()
        #self.object.users.add(self.request.user.profile)
        #self.object.enrolled_users_count += 1
        #self.object.save()
        #return HttpResponseRedirect(self.get_success_url())
@method_decorator(login_required(login_url='/accounts/google/login'), name='dispatch')

class JoinClassListView(ListView):   
    model = StudentClass
    template_name = 'scheduler/all_classes.html'
    context_object_name = 'join_list_of_classes'
    success_url = '/listclasses'
    def get_queryset(self):
        return StudentClass.objects.all()

class JoinClassView(DetailView):
    model = StudentClass
    template_name = 'scheduler/join.html'
    success_url = '/listclasses'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class JoinClassFilterView(ListView):
    model = StudentClass
    template_name ='scheduler/filtered_classes.html'
    context_object_name = "list_of_classes"
    def get_queryset(self):
        return StudentClass.objects.filter(instructor__icontains = self.kwargs['instructor'])

def add_join_class(request, pk):
    studentclass = get_object_or_404(StudentClass, pk=pk)
    studentclass.users.add(request.user.profile)
    if request.user.profile not in studentclass.users.all():
        studentclass.enrolled_users_count += 1
    studentclass.save()
    return HttpResponseRedirect('/listclasses')

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
        context['classmates'] = self.object.users.all()
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

def DeleteNote(request, pk, id):
    note = get_object_or_404(NoteFile, pk=pk)
    note.delete()
    return HttpResponseRedirect(reverse('class_detail', args=(id,)))

def ClassSearch(request):
    return HttpResponseRedirect(reverse('filtered_classes', args=(request.POST['instructor'], )))
'''
def classpage(request, class_id):
    desiredClass = get_object_or_404(StudentClass, pk=class_id)
    return HttpResponseRedirect(reverse('scheduler:class', args = (desiredClass.id,)))
'''


# all_rooms, a function based view that displays all the chat rooms a user is in
# From Kevin Ndung'u, 5/15/2018
# https://www.twilio.com/blog/2018/05/build-chat-python-django-applications-programmable-chat.html
@login_required(login_url='/accounts/google/login')
def all_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})

# room_detail, a function based view that displays the messages in a chat room
# From Kevin Ndung'u, 5/15/2018
# https://www.twilio.com/blog/2018/05/build-chat-python-django-applications-programmable-chat.html
@login_required(login_url='/accounts/google/login')
def room_detail(request, slug):
    room = Room.objects.get(slug=slug)
    return render(request, 'chat/room_detail.html', {'room': room})


# token, a view that allows the app to assign unique tokens to users
# From Kevin Ndung'u, 5/15/2018
# https://www.twilio.com/blog/2018/05/build-chat-python-django-applications-programmable-chat.html
@login_required(login_url='/accounts/google/login')
def token(request):
    identity = request.GET.get('identity', request.user.username)
    device_id = request.GET.get('device', 'default')  # unique device ID

    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY
    api_secret = settings.TWILIO_API_SECRET
    chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID

    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create a unique endpoint ID for the device
    endpoint = "MyDjangoChatRoom:{0}:{1}".format(identity, device_id)

    if chat_service_sid:
        chat_grant = ChatGrant(endpoint_id=endpoint,
                               service_sid=chat_service_sid)
        token.add_grant(chat_grant)

    response = {
        'identity': identity,
        'token': token.to_jwt()
    }

    return JsonResponse(response)

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

