from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from .views import redirect_view

urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    #path('', include('guild_management.urls')),
    path('', redirect_view),
]

admin.site.site_header = 'Guild Manager'
admin.site.site_title = 'Guild Manager'