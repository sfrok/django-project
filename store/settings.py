"""
Django settings for store project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""


import logging
import os

import store.privacy as pc

logger = logging.getLogger('Settings')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = f'{pc.sk}'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []
# ALLOWED_HOSTS = ['*'] #  FOR TESTING ONLY!


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simple_email_confirmation',
    'crispy_forms',
    'baseapp',
]

AUTH_USER_MODEL = 'baseapp.User'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# LOGGING = {
    # 'version': 1,
    # 'disable_existing_loggers': False,
    # 'formatters': {
        # 'simple': {
            # 'format': '[Request] %(message)s'
        # },
    # },
    # 'handlers': {
        # 'console': {
            # 'level': 'INFO',
            # 'class': 'logging.StreamHandler',
            # 'formatter': 'simple'
        # },
    # },
    # 'loggers': {
        # 'django.request': {
            # 'handlers': ['console'],
            # 'level': 'INFO',
            # 'propagate': True,
        # },
    # }
# }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'store.urls'

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

WSGI_APPLICATION = 'store.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': f'django.db.backends.{pc.ADAPTER}',
        'NAME': f'{pc.NAME}',
        'USER': f'{pc.USER}',
        'PASSWORD': f'{pc.PASSWORD}',
        'HOST': f'{pc.HOST}',
        'PORT': f'{pc.PORT}',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# The file storage engine to use when collecting static files
# with the collectstatic management command.

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'baseapp/static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'baseapp/media')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'baseapp/static_dev'),
    os.path.join(BASE_DIR, 'baseapp/media')
)
