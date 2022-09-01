"""
These settings are here to use during tests, because django requires them.

In a real-world use case, apps in this project are installed into other
Django applications, so these settings will not be used.
"""

from os.path import abspath, dirname, join


def root(*args):
    """
    Get the absolute path of the given path relative to the project root.
    """
    return join(abspath(dirname(__file__)), *args)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'default.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'enterprise',
    'common.djangoapps.student',
    'lms.djangoapps.grades',
    'openedx.core.djangoapps.programs',
    'learner_pathway_progress',
    'waffle',
)

LOCALE_PATHS = [
    root('learner_pathway_progress', 'conf', 'locale'),
]

ROOT_URLCONF = 'learner_pathway_progress.api.urls'

SECRET_KEY = 'insecure-secret-key'

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
)

SITE_ID = 1

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': False,
    'OPTIONS': {
        'context_processors': [
            'django.contrib.auth.context_processors.auth',  # this is required for admin
            'django.contrib.messages.context_processors.messages',  # this is required for admin
        ],
    },
}]

USE_TZ = True

LMS_ROOT_URL = "http://localhost:8000"
LMS_ENROLLMENT_API_PATH = "/api/enrollment/v1/"
OAUTH_ID_TOKEN_EXPIRATION = 60 * 60
COURSE_CATALOG_URL_ROOT = 'https://catalog.example.com'
COURSE_CATALOG_API_URL = f'{COURSE_CATALOG_URL_ROOT}/api/v1'
ECOMMERCE_API_URL = 'https://ecommerce.example.com/api/v2/'
ECOMMERCE_PUBLIC_URL_ROOT = None
ENTERPRISE_CATALOG_INTERNAL_ROOT_URL = 'http://enterprise.catalog.app:18160'
ENTERPRISE_ENROLLMENT_API_URL = LMS_ROOT_URL + LMS_ENROLLMENT_API_PATH
LMS_INTERNAL_ROOT_URL = LMS_ROOT_URL
