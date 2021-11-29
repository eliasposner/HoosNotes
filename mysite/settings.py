"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import django_heroku
import os, sys
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&x$ylm06sa3ljo#vkmiffv72aq)pqzpto6dk=h^6ezmwhk2q%%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'bootstrap5',
    'scheduler.apps.SchedulerConfig',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

     #.....................#

    'multiselectfield',

    # Code for configuring django-all-auth applications adapted from Moeedlodhi, 6/21/2021
    # https://medium.com/geekculture/getting-started-with-django-social-authentication-80ee7dc26fe0
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # Code for configuring django REST framework applications
    # https://www.django-rest-framework.org/
    'rest_framework',
    'rest_framework.authtoken',
    
    # Code for deleting media files when the model that uses them is deleted
    #  https://github.com/un1t/django-cleanup
    'django_cleanup.apps.CleanupConfig',


]

# Code for configuring site_id and login_redirect_url adapted from Mudh Rahiman, 2/27/2021
# https://dev.to/mdrhmn/django-google-authentication-using-django-allauth-18f8
SITE_ID = 7
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_ON_GET = True

# Code for configuring authentication credential settings from Moeedlodhi, 6/21/2021
# https://medium.com/geekculture/getting-started-with-django-social-authentication-80ee7dc26fe0
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

# Code for defining template settings from Mudh Rahiman, 2/27/2021
# https://dev.to/mdrhmn/django-google-authentication-using-django-allauth-18f8
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': ['templates/'],
        'DIRS' : [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Code for allowing Github Actions CI to create a test database adapted from user Hybrid, 2/24/14
# https://stackoverflow.com/questions/21978562/django-test-error-permission-denied-to-create-database-using-heroku-postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ddcjlc7o2l88re',
        'USER': 'wivxpbzsnudsrj',
        'PASSWORD': '1d35cbe3b7cd42bafff06afb1b815feac9c146ab686e0f1ba714118382d3ff6d',
        'HOST': 'ec2-54-145-110-118.compute-1.amazonaws.com',
        'PORT': 5432,
    }
}
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'ACee4a95ba8a6b85b49f873fda7a97698e')
TWILIO_API_KEY = os.environ.get('TWILIO_API_KEY', 'SK6369f319577d9bc4d4f4460f32dab412')
TWILIO_API_SECRET = os.environ.get('TWILIO_API_SECRET', 'yM99TM9vdjajPkt6vr69ZslqCD1xXhuX')
TWILIO_CHAT_SERVICE_SID = os.environ.get('TWILIO_CHAT_SERVICE_SID', 'IS0f778b5373fd40b2866c2e60d727f868')


# Code for adding static & media folder directories from Mudh Rahiman, 2/27/2021
# https://dev.to/mdrhmn/django-google-authentication-using-django-allauth-18f8
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
django_heroku.settings(locals())
# This configures the my_adapter file, which handles collisions (when a social account and a regular account has the same email)
# Adapted from Moeedlodhi, 6/21/2021
# https://medium.com/geekculture/getting-started-with-django-social-authentication-80ee7dc26fe0
SOCIALACCOUNT_ADAPTER = 'scheduler.my_adapter.MyAdapter'
