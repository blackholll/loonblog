from settings.common import *
import raven

DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',     # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'loonblognew',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'loonblognew',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',                           # Set to empty string for default.
    }
}


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'formatters': {
            'standard': {
                'format': '%(levelname)s %(asctime)s %(pathname)s %(filename)s %(module)s %(funcName)s %(lineno)d: %(message)s'
            },
        },
        'handlers': {
            'file_handler': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'log/run.log'),
                'formatter': 'standard'
            },
            'console': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
        },
        'loggers': {
            'default': {
                'handlers': ['file_handler', 'console'],
                'propagate': True,
                'level': 'INFO',
            },
            'django.request': {
                'handlers': ['file_handler'],
                'propagate': True,
                'level': 'INFO',
            },
            'django.db.backends': {
                'handlers': ['console'],
                'propagate': True,
                'level': 'INFO',
            }
        }
    }

ENV = 'dev'

# RAVEN_CONFIG = {
#     'dsn': 'https://ca631dccdc58499ea37f1303ea4002c9:cfe607005557469f9a8651347c36197d@sentry.io/187281',
#     # If you are using git, you can also automatically configure the
#     # release based on the git info.
#     'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
# }

# RAVEN_CONFIG = {
#     'dsn': 'https://fb055b02209c47d7b40122c7f244c89b:d411486cbe39459ba4f63488c967c87d@sentry.io/187304',
#     # If you are using git, you can also automatically configure the
#     # release based on the git info.
#     'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
# }
