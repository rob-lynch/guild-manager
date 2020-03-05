from guild_manager.settings.base import *

import django_heroku

SECRET_KEY = os.environ.get('SECRET_KEY')

# Activate Django-Heroku.
django_heroku.settings(locals())


import dj_database_url
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)