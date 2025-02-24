from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, FormView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from juego.models import *
from juego.forms import *
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

class CharacterView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/character.html'

class EquipmentView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/equipment.html'

class FactionView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/faction.html'



class BattleView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/battle.html'


class CharacterDetailView(LoginRequiredMixin, DetailView):
    model = Character

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CharacterListView(LoginRequiredMixin, ListView):
    model = Character
    template_name = 'juego/character_list.html'
    context_object_name = 'character_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        characters = Character.objects.select_related('faction', 'equipped_weapon', 'equipped_armor').all()
        context['character_list'] = characters
        return context


class FactionCharacterFormView(LoginRequiredMixin, FormView):
    template_name = 'juego/faction_character_list.html'
    form_class = FactionForm

    def form_valid(self, form):
        faction = form.cleaned_data["faction"]  # Obtiene la facción seleccionada
        characters = Character.objects.select_related('faction').filter(faction=faction) # Filtra personajes por facción
        return self.render_to_response(self.get_context_data(form=form, characters=characters))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("characters", Character.objects.select_related('faction').all()
)  # Mostrar todos por defecto
        return context

class EquipmentCharacterFormView(LoginRequiredMixin, FormView):
    template_name = 'juego/equipment_character_list.html'
    form_class = EquipmentForm

    def form_valid(self, form):
        weapon = form.cleaned_data["weapon"]  # Obtiene el arma seleccionada
        armor = form.cleaned_data["armor"]  # Obtiene la armadura seleccionada
        characters = Character.objects.select_related('equipped_weapon', 'equipped_armor', 'faction').prefetch_related(
            'inventory__weapons', 'inventory__armors'  # Relaciones de muchos a muchos
        ).all()

        if weapon or armor:
            if weapon and armor:
                characters = characters.filter(equipped_weapon=weapon, equipped_armor=armor)  # Filtros combinados
            elif weapon:
                characters = characters.filter(equipped_weapon=weapon)  # Filtra personajes por arma
            elif armor:
                characters = characters.filter(equipped_armor=armor)  # Filtra personajes por armadura
        else:
            return self.render_to_response(
                (self.get_context_data(form=form, error_mensaje="No has seleccionado ningúna opción")))

        return self.render_to_response(self.get_context_data(form=form, characters=characters))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("characters", Character.objects.all())  # Mostrar todos los personajes por defecto
        context.setdefault("weapons", Weapon.objects.all())  # Mostrar todas las armas por defecto
        context.setdefault("armors", Armor.objects.all())  # Mostrar todas las armaduras por defecto
        return context


class RelationCreateView(LoginRequiredMixin, CreateView):
    model = Relationship
    fields = ['', '']
    template_name = ''
    success_url = ''

class FactionCreateView(LoginRequiredMixin, CreateView):
    model = Faction
    form_class = FactionCreateForm  # Usamos ModelForm
    template_name = 'juego/faction_create.html'
    success_url = reverse_lazy("juego:factionView")

class FactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Faction
    template_name = 'juego/faction_delete.html'
    success_url = reverse_lazy("juego:factionView")

class CharacterCreateView(LoginRequiredMixin, CreateView):
    model = Character
    fields = ['', '']
    template_name = ''
    success_url = ''



class LocationUpdateView(LoginRequiredMixin, UpdateView):
    model = Character
    fields = ['', '']
    template_name = ''
    success_url = ''


class InventoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Character
    fields = ['', '']
    template_name = ''
    success_url = ''

class WeaponListView(LoginRequiredMixin, ListView):
    model = Weapon
    template_name = 'juego/weapon.html'
    context_object_name = 'weapons'


class WeaponDetailView(LoginRequiredMixin, DetailView):
    model = Weapon
    template_name = 'juego/weapon_detail.html'
    context_object_name = 'weapon'

class WeaponCreateView(LoginRequiredMixin, CreateView):
    model = Weapon
    form_class = WeaponForm
    template_name = 'juego/weapon_create.html'
    success_url = reverse_lazy('juego:weaponListView')

class WeaponUpdateView(LoginRequiredMixin, UpdateView):
    model = Weapon
    form_class = WeaponForm
    template_name = 'juego/weapon_form.html'
    success_url = reverse_lazy('juego:weaponListView')

class WeaponDeleteView(LoginRequiredMixin,DeleteView):
    model = Weapon
    template_name = "juego/weapon_delete.html"
    success_url = reverse_lazy('juego:weaponListView')

class ArmorListView(LoginRequiredMixin, ListView, UserPassesTestMixin):
    model = Armor
    template_name = 'juego/armor.html'
    context_object_name = 'armors'


class ArmorDetailView(LoginRequiredMixin, DetailView):
    model = Armor
    template_name = 'juego/armor_detail.html'
    context_object_name = 'armor'

class ArmorCreateView(LoginRequiredMixin, CreateView):
    model = Armor
    form_class = ArmorForm
    template_name = 'juego/armor_create.html'
    success_url = reverse_lazy('juego:armorListView')

class ArmorUpdateView(LoginRequiredMixin, UpdateView):
    model = Armor
    form_class = ArmorForm
    template_name = 'juego/armor_form.html'
    success_url = reverse_lazy('juego:armorListView')

class ArmorDeleteView(LoginRequiredMixin,DeleteView):
    model = Armor
    template_name = "juego/armor_delete.html"
    success_url = reverse_lazy('juego:armorListView')

