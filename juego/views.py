from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms

from juego.models import *
from juego.forms import *
# Create your views here.

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/index.html'

class CharacterDetailView(LoginRequiredMixin, DetailView):
    model = Character

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CharacterListView(ListView):
    model = Character
    template_name = 'juego/character_list.html'
    context_object_name = 'character_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class FactionCharacterFormView(LoginRequiredMixin, FormView):
    template_name = 'juego/faction_character_list.html'
    form_class = FactionForm
    login_url = '/login/'

    def form_valid(self, form):
        faction = form.cleaned_data["faction"] # Obtiene la facción seleccionada
        characters = Character.objects.filter(faction=faction) # Filtra personajes por facción
        return self.render_to_response(self.get_context_data(form=form, characters=characters))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("characters", Character.objects.all())  # Mostrar todos por defecto
        return context

class EquipmentCharacterFormView(LoginRequiredMixin, FormView):
    template_name = 'juego/equipment_character_list.html'
    form_class = EquipmentForm
    login_url = '/login/'

    def form_valid(self, form):
        pass

    def get_context_data(self, **kwargs):
        pass

class BattleView(LoginRequiredMixin, TemplateView):
    template_name = ''


class RelationCreateView(LoginRequiredMixin, CreateView):
    model = Relationship
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



class PersonajeView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/personaje.html'

class EquipamientoView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/equipamiento.html'

class FaccionView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/faccion.html'

class BatallaView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/batalla.html'