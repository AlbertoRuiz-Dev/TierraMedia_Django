from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView


# Create your views here.

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/index.html'

class CharacterListView(LoginRequiredMixin, ListView):
    pass

class FactionCharacterListView(LoginRequiredMixin, ListView):
    pass

class EquipmentCharacterListView(LoginRequiredMixin, ListView):
    pass

class RelationCreateView(LoginRequiredMixin, CreateView):
    pass

class CharacterCreateView(LoginRequiredMixin, CreateView):
    pass

class BattleView(LoginRequiredMixin, TemplateView):
    pass

class WeaponCreateView(LoginRequiredMixin, CreateView):
    pass

class LocationUpdateView(LoginRequiredMixin, UpdateView):
    pass

class InventoryUpdateView(LoginRequiredMixin, UpdateView):
    pass

class EquipmentUpdateView(LoginRequiredMixin, UpdateView):
    pass
