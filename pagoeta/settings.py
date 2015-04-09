"""
Django settings for the project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import json
import os
import sys

from django.conf import global_settings


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Credentials
# If no `CRED_FILE` environment variable is found, we assume we are
# in the DEV environment, and we load a local JSON file
# Local file mimics cloudControl creds
# https://www.cloudcontrol.com/dev-center/platform-documentation#add-ons


if 'CRED_FILE' in os.environ:
    cred_file = os.environ['CRED_FILE']
    DEBUG = False

elif 'BUILDPACK_RUNNING' in os.environ:
    cred_file = os.path.join(BASE_DIR, 'creds.json.txt')
    DEBUG = False

else:
    cred_file = os.path.join(BASE_DIR, 'creds.json')
    DEBUG = True

# Load and massage credentials
cred_data = open(cred_file)
creds = json.load(cred_data)
cred_data.close()
CONFIG_VARS = creds['CONFIG']['CONFIG_VARS']


# Allowed hosts

if DEBUG:
    ALLOWED_HOSTS = ('localhost',)
    INTERNAL_IPS = ('127.0.0.1',)
else:
    ALLOWED_HOSTS = ('pagoeta.cloudcontrolled.com', '.pagoeta.cloudcontrolled.com')
    HOST = 'pagoeta.cloudcontrolled.com'


# Development settings
# https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/
# https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-ADMINS

SECRET_KEY = CONFIG_VARS['secret']
ADMINS = (('eillarra', 'eneko@illarra.com'),)

TEMPLATE_DEBUG = DEBUG
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'pagoeta/templates'),
)


# Application definition

INSTALLED_APPS = (
    # Translations
    'hvad',
    # Helpers
    'djrill',
    'imagekit',
    'markdown_deux',
    'storages',
    'wkhtmltopdf',
    # Default Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    # Custom apps
    'rest_framework',
    'pagoeta.apps.core',
    'pagoeta.apps.places',
    'pagoeta.apps.events',
    'pagoeta.apps.health',
    'pagoeta.apps.forecast',
    'pagoeta.apps.posts',
    # Admin
    'grappelli',
    'easy_select2',
    #'pagedown', Fix this when package is fixed
    'django.contrib.admin',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'pagoeta.apps.core.middleware.LanguageOnQueryParamMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
else:
    INSTALLED_APPS += ('gunicorn',)

ROOT_URLCONF = 'pagoeta.urls'
WSGI_APPLICATION = 'pagoeta.wsgi.application'


# Site host is set here to provide a way to have
# absolute URLs in the API, without having access to the `request`
# object or make extra queries.

SITE_HOST = CONFIG_VARS['site_host']


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': creds['MYSQLS']['MYSQLS_DATABASE'],
        'USER': creds['MYSQLS']['MYSQLS_USERNAME'],
        'PASSWORD': creds['MYSQLS']['MYSQLS_PASSWORD'],
        'HOST': creds['MYSQLS']['MYSQLS_HOSTNAME'],
        'PORT': creds['MYSQLS']['MYSQLS_PORT'],
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB,character_set_connection=utf8,collation_connection=utf8_unicode_ci;',
        }
    }
}


# REST API
# http://www.django-rest-framework.org/

REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'URL_FIELD_NAME': 'href'
}

if not DEBUG:
    REST_FRAMEWORK.update({
        'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    })

# CACHE
# https://docs.djangoproject.com/en/1.8/topics/cache/

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}

CACHE_MIDDLEWARE_SECONDS = 300


# Email
# https://docs.djangoproject.com/en/1.8/topics/email/

MANDRILL_API_KEY = CONFIG_VARS['mandrill__test_key'] if DEBUG else CONFIG_VARS['mandrill__production_key']

EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = CONFIG_VARS['mandrill__username']
EMAIL_HOST_PASSWORD = MANDRILL_API_KEY
EMAIL_USE_TLS = True

EMAIL_SUBJECT_PREFIX = '[Pagoeta API] '
DEFAULT_FROM_EMAIL = 'Pagoeta <pagoeta@zarautz.org>'
SERVER_EMAIL = 'root@zarautz.org'


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'eu'
USE_L10N = True

USE_I18N = True
LANGUAGES = (
    ('eu', 'Basque'),
    ('es', 'Spanish'),
    ('en', 'English'),
    ('fr', 'French'),
)


# Time zones
# https://docs.djangoproject.com/en/1.8/topics/i18n/timezones/

USE_TZ = True
TIME_ZONE = 'Europe/Madrid'


# Media
# wkhtmltopdf requires MEDIA configuration to be set
# http://stackoverflow.com/questions/24071290/
# https://docs.djangoproject.com/en/1.8/ref/settings/#media-root
# https://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html

AWS_HEADERS = { # see http://developer.yahoo.com/performance/rules.html#expires
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}
AWS_STORAGE_BUCKET_NAME = CONFIG_VARS['aws__bucket_name']
AWS_ACCESS_KEY_ID = CONFIG_VARS['aws__access_key_id']
AWS_SECRET_ACCESS_KEY = CONFIG_VARS['aws__secret_access_key']
AWS_S3_URL = 'https://%s.%s' % (AWS_STORAGE_BUCKET_NAME, CONFIG_VARS['aws__s3_host'])

MEDIA_URL = '%s/media/' % AWS_S3_URL
DEFAULT_FILE_STORAGE = 'pagoeta.s3_utils.MediaS3BotoStorage'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
# https://docs.djangoproject.com/en/1.8/howto/static-files/deployment/
# http://whitenoise.readthedocs.org/en/latest/index.html

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'pagoeta/static'),
)

if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
    WHITENOISE_ROOT = os.path.join(BASE_DIR, 'staticfiles/www')


# wkhtmltopdf
# http://django-wkhtmltopdf.readthedocs.org/en/latest/

WKHTMLTOPDF_CMD = '/usr/local/bin/wkhtmltopdf'
WKHTMLTOPDF_CMD_OPTIONS = {
    'quiet': True,
}

# Markdown

MARKDOWN_EDITOR_SKIN = 'simple'


# Administration area
# https://docs.djangoproject.com/en/1.8/ref/contrib/admin/
# http://django-grappelli.readthedocs.org/en/latest/index.html

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django.core.context_processors.media',
)

FIRST_DAY_OF_WEEK = 1
DATE_FORMAT = 'N j, Y'
TIME_FORMAT = 'H:i'
DATETIME_FORMAT = DATE_FORMAT +', '+ TIME_FORMAT

GRAPPELLI_ADMIN_TITLE = 'Pagoeta API'
GRAPPELLI_CLEAN_INPUT_TYPES = False
