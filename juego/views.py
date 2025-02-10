from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from juego.models import *
from juego.forms import *
from django.views.generic import TemplateView, CreateView


# Create your views here.

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/index.html'

class PersonajeView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/personaje.html'

class EquipamientoView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/equipamiento.html'

class FaccionView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/faccion.html'

class BatallaView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/batalla.html'

class RelacionesFormView(LoginRequiredMixin, CreateView):
    template_name = 'juego/relation.html'
    form_class = RelationForm



    def form_valid(self, form):
        relation = form.cleaned_data["relation_type"]
        return self.render_to_response(self.get_context_data(form=form, relation=relation))



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

    def form_valid(self, form):
        weapon = form.cleaned_data["weapon"]  # Obtiene el arma seleccionada
        armor = form.cleaned_data["armor"]  # Obtiene la armadura seleccionada
        characters = Character.objects.all()

        if weapon or armor:
            if weapon:
                characters = characters.filter(equipped_weapon=weapon)  # Filtra personajes por arma
            if armor:
                characters = characters.filter(equipped_armor=armor) # Filtra personajes por armadura
        else:
            return self.render_to_response((self.get_context_data(form=form, error_mensaje="No has seleccionado ningúna opción")))

        return self.render_to_response(self.get_context_data(form=form, characters=characters))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("characters", Character.objects.all())  # Mostrar todos los personajes por defecto
        context.setdefault("weapons", Weapon.objects.all())  # Mostrar todas las armas por defecto
        context.setdefault("armors", Armor.objects.all())  # Mostrar todas las armaduras por defecto
        return context

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



