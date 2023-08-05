import os
import sys

SITE_ID = 1
DEBUG = True

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)
sys.path.insert(0,os.path.join(BASE_DIR, 'apps'))

MEDIA_ROOT = os.path.normcase(os.path.dirname(os.path.abspath(__file__)))
MEDIA_URL = '/media/'

DATABASE_ENGINE = 'sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'drf_example',
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.auth',
    'rest_framework',
    'polymorphic',
    'example',
    'debug_toolbar',
    'django_filters',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_URL = '/static/'

ROOT_URLCONF = 'example.urls'

SECRET_KEY = 'abc123'

PASSWORD_HASHERS = ('django.contrib.auth.hashers.UnsaltedMD5PasswordHasher', )

MIDDLEWARE = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ('127.0.0.1', )

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'EXCEPTION_HANDLER': 'rest_framework_app_api.exceptions.exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_app_api.pagination.JsonApiPageNumberPagination',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
}
