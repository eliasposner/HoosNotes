from django.shortcuts import render


# https://dev.to/mdrhmn/django-google-authentication-using-django-allauth-18f8
def view_name(request):
    return render(request, 'scheduler/index.html', {})