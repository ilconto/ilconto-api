"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import datetime
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*8-)+e*1**vw7ala(9^o99l*n4v7=m!&fy!$v@xzyrt$*0cm^2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.postgres',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'boards.apps.BoardsConfig',
    'django_extensions',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth.registration',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

if 'TRAVIS' not in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config("DB_NAME"),
            'USER': config("DB_USER", default="postgres"),
            'PASSWORD': config("DB_PASSWORD", default="postgres"),
            'HOST': config("DB_HOST", default="0.0.0.0"),
            'PORT': config("DB_PORT", default=5432),
        },
        'origin': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else :
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql_psycopg2',
            'NAME':     'ilcontodb',
            'USER':     'postgres',
            'PASSWORD': '',
            'HOST':     'localhost',
            'PORT':     '',
        }
    }



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'boards.AppUser'

# django-rest-auth login settings
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGIN_ON_CONFIRM = False
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'api/v1/rest-auth/login'
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'boards.serializers.AppUserSerializer',
}

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = config('EMAIL_APP_ADDRESS')
EMAIL_HOST_PASSWORD = config('EMAIL_APP_PWD')
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_FROM = EMAIL_HOST_USER
EMAIL_SUBJECT_PREFIX = '[Ilconto] '
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_ID = 1
