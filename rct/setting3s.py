"""
Settings ini untuk deployment ke Heroku
"""

import os
import dj_database_url 
import django_heroku
import cloudinary
import cloudinary_storage
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hf2zmy6*a!sq-=_v5l4lo@($a#)o3mj^*!oa6at9h&8y18@(u7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['django-rct.herokuapp.com','localhost','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rct.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rct.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # 'ENGINE': 'djongo',
        'NAME': 'd94smpli3brt6t',
        'HOST': 'ec2-52-1-115-6.compute-1.amazonaws.com',
        'USER': 'wfwluxeadhbcju',
        'PORT': 5432,
        'PASSWORD': '3f7ef6a95acb4db58e6e521c0a831ce2f54563145b3d9be8baf38b4679d04fa6'
    }
}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'id-ID'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# CLOUDINARY = {
#   'cloud_name': 'django-rct',  
#   'api_key': '367531534655924',  
#   'api_secret': 'sgWc7hANJiaZ6DSUJsi1AT6B_bI',  
# }

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

PROJECT_ROOT   =   BASE_DIR
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'masuk'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

AUTH_USER_MODEL = 'app.User'

#  Add configuration for static files storage using whitenoise
STATIC_ROOT  =   os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUD_NAME', default="django-rct"),
    'API_KEY': config('API_KEY', default="367531534655924"),
    'API_SECRET': config('API_SECRET', default="sgWc7hANJiaZ6DSUJsi1AT6B_bI"),
}



prod_db  =  dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)

# django_heroku.settings(locals())