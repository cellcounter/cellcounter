import os
import uuid

import dj_database_url

DEBUG = bool(os.environ.get('DEBUG', False))
TEST = bool(os.environ.get('TEST', False))
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
PROJECT_DIR = os.path.dirname(__file__)

DEFAULT_DATABASE_URL = "sqlite:///%s" % os.path.join(PROJECT_DIR, 'db.sqlite3')

if TEST:
    # Need to disable rate limiting for test purposes
    if not bool(os.environ.get('TRAVIS', False)):
        DEFAULT_DATABASE_URL = 'sqlite://:memory:'
    RATELIMIT_ENABLE = False

# Change default address if env-var is set
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'webmaster@localhost')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

DATABASES = {'default': dj_database_url.config(default=DEFAULT_DATABASE_URL)}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, '../media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, '../static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
# STATICFILES_DIRS = (os.path.join(PROJECT_DIR, 'static'),)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', str(uuid.uuid4()))

# Logins URLs
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/logout/'

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'cellcounter.statistics.middleware.StatsSessionMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ratelimit.middleware.RatelimitMiddleware',
)

# HTTPS_SUPPORT = True
HTTPS_SUPPORT = False

SECURE_REQUIRED_PATHS = (
    # '/admin/',
    # '/count/',
    # '/login/',
    # '/accounts/',
)

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

ROOT_URLCONF = 'cellcounter.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'cellcounter.wsgi.application'

# Template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'colorful',
    'rest_framework',
    'compressor',
    'cellcounter.main',
    'cellcounter.cc_kapi',
    'cellcounter.accounts',
    'cellcounter.statistics'
)

CACHES = {'default': {}}

if DEBUG or TEST:
    CACHES['default']['BACKEND'] = 'django.core.cache.backends.locmem.LocMemCache'
else:
    CACHES['default']['BACKEND'] = 'django.core.cache.backends.memcached.PyLibMCCache'
    CACHES['default']['LOCATION'] = os.environ.get('MEMCACHED_LOCATION')

RATELIMIT_VIEW = 'cellcounter.accounts.views.rate_limited'

# Logging config

if 'ENABLE_DJANGO_LOGGING' in os.environ:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(funcName)s %(lineno)d %(message)s'
            }
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'filters': ['require_debug_false'],
            },
            'logfile': {
                'class': 'logging.handlers.WatchedFileHandler',
                'filename': os.environ.get('DJANGO_LOG_PATH'),
                'formatter': 'verbose'
            },
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
                'propagate': False,
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
                'propagate': True,
            },
            'cellcounter': {
                'handlers': ['mail_admins', 'console'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
                'propagate': False
            },
        }
    }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    )
}

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Store session cookies for 1 week only
SESSION_COOKIE_AGE = 604800

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
