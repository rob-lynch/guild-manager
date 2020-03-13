from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from .views import redirect_view
import os

urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    #path('', include('guild_management.urls')),
    path('', redirect_view),
]

if 'SITE_HEADER' in os.environ:
    admin.site.site_header = os.environ['SITE_HEADER']
else:
    admin.site.site_header = "Guild Manager"

if 'SITE_TITLE' in os.environ:
    admin.site.site_title =  os.environ['SITE_TITLE']
else:
    admin.site.site_title = "Guild Manager"
