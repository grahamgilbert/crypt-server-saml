# Django settings for Crypt project.
from settings_import import ADMINS, TIME_ZONE, LANGUAGE_CODE, ALLOWED_HOSTS, DISPLAY_NAME, DEBUG
from system_settings import *
from os import path
import saml2
from saml2.saml import NAMEID_FORMAT_PERSISTENT
import logging
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))

SAML_DJANGO_USER_MAIN_ATTRIBUTE = 'email'
SAML_USE_NAME_ID_AS_USERNAME = True
SAML_CREATE_UNKNOWN_USER = True
SAML_ATTRIBUTE_MAPPING = {
    'uid': ('username', ),
    'mail': ('email', ),
    'cn': ('first_name', ),
    'sn': ('last_name', ),
}

if DEBUG == True:

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'djangosaml2.backends.Saml2Backend',
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_DIR, 'db/sal.db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# PG Database
host = None
port = None

if os.environ.has_key('DB_HOST'):
    host = os.environ('DB_HOST')
    port = os.environ.get('DB_PORT')

elif os.environ.has_key('DB_PORT_5432_TCP_ADDR'):
    host = os.environ('DB_PORT_5432_TCP_ADDR')
    port = os.environ.get('DB_PORT_5432_TCP_PORT', '5432')

if host and port:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASS'],
            'HOST': host,
            'PORT': port,
        }
    }

BASEDIR = path.dirname(path.abspath(__file__))
SAML_CONFIG = {
  # full path to the xmlsec1 binary programm
  'xmlsec_binary': '/usr/bin/xmlsec1',

  # your entity id, usually your subdomain plus the url to the metadata view
  'entityid': 'http://YOU/saml2/metadata/',

  # directory with attribute mapping
  'attribute_map_dir': path.join(BASEDIR, 'attributemaps'),

  # this block states what services we provide
  'service': {
      # we are just a lonely SP
      'sp' : {
          'authn_requests_signed': False,
          "allow_unsolicited": True,
          'want_assertions_signed': True,
          'allow_unknown_attributes': True,
          'name': 'Federated Django sample SP',
          'name_id_format': NAMEID_FORMAT_PERSISTENT,
          'endpoints': {
              # url and binding to the assetion consumer service view
              # do not change the binding or service name
              'assertion_consumer_service': [
                  ('http://YOU/saml2/acs/',
                   saml2.BINDING_HTTP_POST),
                  ],
              # url and binding to the single logout service view
              # do not change the binding or service name
              'single_logout_service': [
                  ('http://YOU/saml2/ls/',
                   saml2.BINDING_HTTP_REDIRECT),

                  ('http://YOU/saml2/ls/post',
                   saml2.BINDING_HTTP_POST),
                  ],
              },

           # attributes that this project need to identify a user
          'required_attributes': ['uid'],

           # attributes that may be useful to have but not required
          # 'optional_attributes': ['eduPersonAffiliation'],

          # in this section the list of IdPs we talk to are defined
          'idp': {
              # we do not need a WAYF service since there is
              # only an IdP defined here. This IdP should be
              # present in our metadata

              # the keys of this dictionary are entity ids
              'https://YOURID: {
                  'single_sign_on_service': {
                      saml2.BINDING_HTTP_REDIRECT: 'https://YOURSSOURL',
                      },
                  'single_logout_service': {
                      saml2.BINDING_HTTP_REDIRECT: 'https://YOURSLOURL',
                      },
                  },
              },
          },
      },

  # where the remote metadata is stored
  'metadata': {
      'local': [path.join(BASEDIR, 'metadata.xml')],
      },

  # set to 1 to output debugging information
  'debug': 1,

  # certificate
  # 'key_file': path.join(BASEDIR, 'mycert.key'),  # private part
  # 'cert_file': path.join(BASEDIR, 'mycert.pem'),  # public part

  # own metadata settings
  # 'contact_person': [
  #     {'given_name': 'Lorenzo',
  #      'sur_name': 'Gil',
  #      'company': 'Yaco Sistemas',
  #      'email_address': 'lgs@yaco.es',
  #      'contact_type': 'technical'},
  #     {'given_name': 'Angel',
  #      'sur_name': 'Fernandez',
  #      'company': 'Yaco Sistemas',
  #      'email_address': 'angel@yaco.es',
  #      'contact_type': 'administrative'},
  #     ],
  # you can set multilanguage information here
  # 'organization': {
  #     'name': [('Someone', 'en'),
  #     'display_name': [('Someone', 'en')],
  #     'url': [('http://www.someone.com', 'en')],
  #     },
  'valid_for': 24,  # how long is our metadata valid
  }

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
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
# deprecated in Django 1.4, but django_wsgiserver still looks for it
# when serving admin media
ADMIN_MEDIA_PREFIX = '/static_admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'site_static'),
)

LOGIN_URL='/saml2/login/'
LOGIN_REDIRECT_URL='/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ALLOWED_HOSTS = ['*']

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'SETTHISVALUE'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'fvserver.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'fvserver.wsgi.application'
ENCRYPTED_FIELD_KEYS_DIR = os.path.join(PROJECT_DIR, 'keyset')

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'server',
    'bootstrap3',
    'django_extensions',
)

INSTALLED_APPS += ('djangosaml2',)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS':True,
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
            'debug': DEBUG,
        },
    },
]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
