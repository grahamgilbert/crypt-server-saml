# Django settings for Crypt project.
from settings_import import ADMINS, TIME_ZONE, LANGUAGE_CODE, ALLOWED_HOSTS, DISPLAY_NAME, DEBUG
from system_settings import *
from os import path
import saml2
from saml2.saml import NAMEID_FORMAT_PERSISTENT
import logging
import sys

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

INSTALLED_APPS += ('djangosaml2',)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'djangosaml2.backends.Saml2Backend',
)

LOGIN_URL = '/saml2/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

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
  'attribute_map_dir': path.join(BASEDIR, 'attribute-maps'),

  # this block states what services we provide
  'service': {
      # we are just a lonely SP
      'sp' : {
          'authn_requests_signed': False,
          "allow_unsolicited": True,
          'want_assertions_signed': False,
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
