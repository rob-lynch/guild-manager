import django_filters

from django.http import HttpResponse
from django_tables2 import SingleTableView
from django_filters.views import FilterView
from django.shortcuts import render 
from django_tables2.views import SingleTableMixin
from tablib import Dataset

from .models import Character
from .tables import CharacterTable
from .resources import CharacterResource
class CharacterListView(SingleTableView):
    model = Character
    table_class = CharacterTable
    template_name = 'attendance.html'

class CharacterFilter(django_filters.FilterSet):
    class Meta:
        model = Character
        fields = ['name','rank','playable_class']

class FilteredCharacterListView(SingleTableMixin, FilterView):
    table_class = CharacterTable
    model = Character
    template_name = "attendance.html"

    filterset_class = CharacterFilter

