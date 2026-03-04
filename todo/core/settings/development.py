"""
Django development settings.
"""

from .base import *

SECRET_KEY = 'django-insecure-@%+d^jwivjidp7&n*zznlcuzb^s_y6se)482t&n7(&08nsblh@'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5173',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:5173',
]
