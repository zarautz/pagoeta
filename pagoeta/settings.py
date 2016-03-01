"""
Django settings for the project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import dj_database_url
import json
import os

from django.conf import global_settings


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Credentials
# If no `app__secret_key` environment variable is found, we assume we are
# in the DEV environment, and we load a local JSON file

if 'app__secret_key' in os.environ:
    config_file = None
    DEBUG = False
    ALLOWED_HOSTS = ('data.zarautz.xyz', 'pagoeta.illarra.com')  # pagoeta.illarra.com is the legacy URL, to remove

elif 'TRAVIS' in os.environ:
    config_file = os.path.join(BASE_DIR, 'config.json.txt')
    DEBUG = False
    ALLOWED_HOSTS = ['*']

else:
    config_file = os.path.join(BASE_DIR, 'config.json')
    DEBUG = True
    ALLOWED_HOSTS = ('localhost',)
    INTERNAL_IPS = ('127.0.0.1',)

# Load config variables
if config_file:
    config_data = open(config_file)
    CONFIG_VARS = json.load(config_data)
    config_data.close()

    if 'TRAVIS' in os.environ:
        """TRAVIS needs the MagicSeaWeed API key to complete the tests. This is added as ENV variable."""
        CONFIG_VARS['magicseaweed__api_key'] = os.environ.get('magicseaweed__api_key')
else:
    CONFIG_VARS = {
        'app__postgresql_url': os.environ.get('DATABASE_URL'),
        'app__secret_key': os.environ.get('app__secret_key'),
        'app__site_host': os.environ.get('app__site_host'),
        'aws__access_key_id': os.environ.get('aws__access_key_id'),
        'aws__bucket_name': os.environ.get('aws__bucket_name'),
        'aws__s3_host': os.environ.get('aws__s3_host'),
        'aws__secret_access_key': os.environ.get('aws__secret_access_key'),
        'magicseaweed__api_key': os.environ.get('magicseaweed__api_key'),
        'magicseaweed__secret_key': os.environ.get('magicseaweed__secret_key'),
        'mandrill__production_key': os.environ.get('mandrill__production_key'),
        'mandrill__subaccount': os.environ.get('mandrill__subaccount'),
        'mandrill__test_key': os.environ.get('mandrill__test_key'),
        'mandrill__username': os.environ.get('mandrill__username'),
    }


# Development settings
# https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/
# https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-ADMINS

SECRET_KEY = CONFIG_VARS['app__secret_key']
ADMINS = (('eillarra', 'eneko@zarautz.xyz'),)

TEMPLATE_DEBUG = DEBUG
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'pagoeta/templates'),
)


# Application definition

INSTALLED_APPS = (
    # Translations
    'modeltranslation',
    # Helpers
    'corsheaders',
    'djrill',
    'imagekit',
    'storages',
    'wkhtmltopdf',
    # Admin
    'grappelli',
    'django.contrib.admin',
    # Default Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    # Custom apps
    'rest_framework',
    'rest_framework_swagger',
    'pagoeta.apps.core',
    'pagoeta.apps.places',
    'pagoeta.apps.events',
    'pagoeta.apps.health',
    'pagoeta.apps.forecast',
    'pagoeta.apps.posts',
)

# http://stackoverflow.com/questions/4632323/practical-rules-for-django-middleware-ordering

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'pagoeta.apps.core.middleware.LanguageOnQueryParamMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
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

SITE_HOST = CONFIG_VARS['app__site_host']


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default=CONFIG_VARS['app__postgresql_url'])
}

if 'TRAVIS' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'pagoeta_test',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        }
    }


# REST API
# http://www.django-rest-framework.org/

REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'URL_FIELD_NAME': 'href',
    'COERCE_DECIMAL_TO_STRING': False,
    'TIME_FORMAT': '%H:%M'
}

if not DEBUG:
    REST_FRAMEWORK.update({
        'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    })

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = ('GET', 'OPTIONS')

SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': '1.0',
    'enabled_methods': ('get',),
    'info': {
        'title': 'Pagoeta API',
        'description': '`Pagoeta` is the public API of the city of Zarautz, Basque Country. '
                       'The information you can find here is free for you to use in your applications, '
                       'but please be gentle with our server (you should cache this results on your side too). '
                       'All data is made available under the Open Database License: '
                       'http://opendatacommons.org/licenses/odbl/1.0/. '
                       'Whenever external sources are mentioned you should mention them too.',
    },
}


# CACHE
# https://docs.djangoproject.com/en/1.8/topics/cache/

if not DEBUG and 'TRAVIS' not in os.environ:
    CACHES = {
        'default': {
            'BACKEND': 'django_bmemcached.memcached.BMemcached',
            'LOCATION': os.environ.get('MEMCACHEDCLOUD_SERVERS').split(','),
            'OPTIONS': {
                'username': os.environ.get('MEMCACHEDCLOUD_USERNAME'),
                'password': os.environ.get('MEMCACHEDCLOUD_PASSWORD')
            }
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

CACHE_MIDDLEWARE_SECONDS = 300
USE_ETAGS = True


# Email
# https://docs.djangoproject.com/en/1.8/topics/email/

MANDRILL_API_KEY = CONFIG_VARS['mandrill__test_key'] if DEBUG else CONFIG_VARS['mandrill__production_key']
MANDRILL_SUBACCOUNT = CONFIG_VARS['mandrill__subaccount']

EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = CONFIG_VARS['mandrill__username']
EMAIL_HOST_PASSWORD = MANDRILL_API_KEY
EMAIL_USE_TLS = True

EMAIL_SUBJECT_PREFIX = '[Pagoeta API] '
DEFAULT_FROM_EMAIL = 'Pagoeta <pagoeta@zarautz.xyz>'
SERVER_EMAIL = 'root@zarautz.xyz'


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'eu'
MODELTRANSLATION_DEFAULT_LANGUAGE = LANGUAGE_CODE
USE_L10N = True

USE_I18N = True
LANGUAGES = (
    ('eu', 'Basque'),
    ('es', 'Spanish'),
    ('en', 'English'),
    ('fr', 'French'),
)

LOCALE_PATHS = (os.path.join(BASE_DIR, 'pagoeta/locale'),)


# Time zones
# https://docs.djangoproject.com/en/1.8/topics/i18n/timezones/

USE_TZ = True
TIME_ZONE = 'Europe/Madrid'


# Media
# wkhtmltopdf requires MEDIA configuration to be set
# http://stackoverflow.com/questions/24071290/
# https://docs.djangoproject.com/en/1.8/ref/settings/#media-root
# https://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html

AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
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

if not DEBUG and 'TRAVIS' not in os.environ:
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
    WHITENOISE_ROOT = os.path.join(BASE_DIR, 'staticfiles/www')


# wkhtmltopdf
# http://django-wkhtmltopdf.readthedocs.org/en/latest/
# https://pypi.python.org/pypi/wkhtmltopdf-pack

WKHTMLTOPDF_CMD = 'wkhtmltopdf' if DEBUG else 'wkhtmltopdf-pack'
WKHTMLTOPDF_CMD_OPTIONS = {
    'quiet': True,
    'page-size': 'A4',
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
DATETIME_FORMAT = DATE_FORMAT + ', ' + TIME_FORMAT

GRAPPELLI_ADMIN_TITLE = 'Pagoeta API'
GRAPPELLI_CLEAN_INPUT_TYPES = False


# EXTERNAL API KEYS

MAGICSEAWEED_API_KEY = CONFIG_VARS['magicseaweed__api_key']
MAGICSEAWEED_SECRET_KEY = CONFIG_VARS['magicseaweed__secret_key']


# Zarautz settings

ZARAUTZ_LATITUDE = 43.284410
ZARAUTZ_LONGITUDE = -2.172193
