from settings.common import *
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DEBUG = True
ALLOWED_HOSTS = []

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

ENV = 'test'
