from guild_manager.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sgochm@n^-uuv!ce%^^dqj5h*z6!ajjxyml&_!hx&r7@0e1#xd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'guild_manager',
        'USER': 'guild_manager',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'MAX_ENTRIES': 5000
        },
        'TIMEOUT': 300,
    },
}