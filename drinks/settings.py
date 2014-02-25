"""
Django settings for drinks project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
EMAIL_HOST = 'smtp.adelaide.edu.au'
EMAIL_PORT = '25'
with open(os.path.join(BASE_DIR, 'secret.key')) as f:
    SECRET_KEY = f.readline()
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = ('django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'homebrew')
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware')
ROOT_URLCONF = 'drinks.urls'
WSGI_APPLICATION = 'drinks.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3',
             'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
             'ATOMIC_REQUESTS': True}}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'homebrew/static'),)
LOGIN_URL = '/accounts/login/'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
