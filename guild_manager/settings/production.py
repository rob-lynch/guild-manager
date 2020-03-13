from guild_manager.settings.base import *

import django_heroku

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

# Activate Django-Heroku.
django_heroku.settings(locals())

import dj_database_url
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

redis_location = os.environ['REDIS_URL']

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': redis_location,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'MAX_ENTRIES': 5000
        },
        'TIMEOUT': 3600,
    },
}