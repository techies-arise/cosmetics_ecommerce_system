import os
from pathlib import Path
import sys
from .base import *

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))



# Overriding global baselines safely for local coding

DEBUG = True

# The Docker-created log file may be owned by root on the host. In development,
# use the console handler only so local commands don't fail on file permissions.
LOGGING = {
    **LOGGING,
    'handlers': {
        name: handler
        for name, handler in LOGGING['handlers'].items()
        if name != 'file'
    },
    'loggers': {
        **LOGGING['loggers'],
        'django': {
            **LOGGING['loggers']['django'],
            'handlers': ['console'],
        },
    },
}

ALLOWED_HOSTS = ['*']

# Database routing for Docker MySQL service
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'cosmetics_db'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

# To print emails to the console instead of sending them to real users
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}