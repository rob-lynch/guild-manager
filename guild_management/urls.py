from django.urls import path

from . import views

urlpatterns = [
    path('', views.FilteredCharacterListView.as_view())
]

