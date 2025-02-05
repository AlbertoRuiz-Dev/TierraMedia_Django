from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from juego.models import *

# Create your views here.

"""

    Pagina principal donde se muestra un menu con las diferentes funciones
    Pagina para el login/logout

    Opcion personaje
    Pagina para crear el personaje
    Pagina para crear las relaciones
    Pagina para mostrar los personajes de una faccion
    Pagina para mostrar los personajes segun un equipamiento
    Pagina para mostrar todos los personajes
    Pagina para las batallas
    Pagina para modificar inventario
    Pagina para modificar equipamiento
    Pagina para cambiar la localizacion
    Pagina para crear las armas
    Pagina para mostrar los detalles de un jugador

"""

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/index.html'

class CharacterDetailView(LoginRequiredMixin, DetailView):
    model = Character

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

class CharacterListView(LoginRequiredMixin, ListView):
    model = Character
    template_name = ''
    context_object_name = ''

    def get_queryset(self):
        pass

class FactionCharacterListView(LoginRequiredMixin, ListView):
    model = Faction
    template_name = ''
    context_object_name = ''

    def get_queryset(self):
        pass

class EquipmentCharacterListView(LoginRequiredMixin, ListView):
    model = Equipment
    template_name = ''
    context_object_name = ''

    def get_queryset(self):
        pass

class BattleView(LoginRequiredMixin, TemplateView):
    template_name = ''


class RelationCreateView(LoginRequiredMixin, CreateView):
    model = Relation
    fields = ['','']
    template_name = ''
    success_url = ''

class CharacterCreateView(LoginRequiredMixin, CreateView):
    model = Character
    fields = ['','']
    template_name = ''
    success_url = ''

class WeaponCreateView(LoginRequiredMixin, CreateView):
    model = Weapon
    fields = ['','']
    template_name = ''
    success_url = ''

class LocationUpdateView(LoginRequiredMixin, UpdateView):
    model = Character
    fields = ['','']
    template_name = ''
    success_url = ''

class InventoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Character
    fields = ['','']
    template_name = ''
    success_url = ''

class EquipmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Equipment
    fields = ['','']
    template_name = ''
    success_url = ''
