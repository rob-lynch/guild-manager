from guild_manager.settings.base import *
from django.utils.crypto import get_random_string
import django_heroku

chars='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
SECRET_KEY=get_random_string(50, chars)

DEBUG = True

# Activate Django-Heroku.
django_heroku.settings(locals())


import dj_database_url
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)