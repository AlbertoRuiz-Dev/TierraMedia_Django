from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, FormView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from juego.models import *
from juego.forms import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from juego.models import Character
from juego.serializers import CharacterSerializer

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


@api_view(['GET'])
def get_data(request):
    datos = Character.objects.select_related('faction', 'equipped_weapon', 'equipped_armor').all()
    serializer = CharacterSerializer(datos, many=True)
    return Response(serializer.data)


class BattleView(LoginRequiredMixin, FormView):
    template_name = 'juego/battle.html'
    form_class = CharacterBattleForm


class CharacterDetailView(LoginRequiredMixin, DetailView):
    model = Character
    template_name = "juego/character_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CharacterUpdateView(LoginRequiredMixin, UpdateView):
    model = Character
    form_class = CharacterForm
    template_name = 'juego/character_update.html'
    success_url = reverse_lazy("juego:characterView")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.object and hasattr(self.object, 'inventory'):
            # Limit equipped_weapon to weapons in the character's inventory
            form.fields['equipped_weapon'].queryset = self.object.inventory.weapons.all()
            # Limit equipped_armor to armors in the character's inventory
            form.fields['equipped_armor'].queryset = self.object.inventory.armors.all()
        return form

class CharacterListView(LoginRequiredMixin, ListView):
    model = Character
    template_name = 'juego/character.html'
    context_object_name = 'character_list'

class CharacterDeleteView(LoginRequiredMixin, DeleteView):
    model = Character
    template_name = 'juego/character_delete.html'
    success_url = reverse_lazy("juego:factionView")

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
    form_class = FactionDefaultForm  # Usamos ModelForm
    template_name = 'juego/faction_create.html'
    success_url = reverse_lazy("juego:factionView")

class FactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Faction
    form_class = FactionDefaultForm
    template_name = 'juego/faction_update.html'
    success_url = reverse_lazy("juego:factionView")

class FactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Faction
    template_name = 'juego/faction_delete.html'
    success_url = reverse_lazy("juego:factionView")

class CharacterCreateView(LoginRequiredMixin, CreateView):
    model = Character
    form_class = CharacterForm
    template_name = 'juego/character_create.html'
    success_url = reverse_lazy('characterListView')

    def form_valid(self, form):
        # Create the character first
        self.object = form.save()
        # Create an associated Inventory instance
        Inventory.objects.create(character=self.object)
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # For new characters, equipped_weapon and equipped_armor should default to None or empty
        form.fields['equipped_weapon'].queryset = Weapon.objects.none()
        form.fields['equipped_armor'].queryset = Armor.objects.none()
        return form


class LocationUpdateView(LoginRequiredMixin, UpdateView):
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

class InventoryAddWeaponView(LoginRequiredMixin, FormView):
    template_name = 'juego/inventory_add_weapon.html'
    success_url = reverse_lazy('juego:characterDetailView')

    def get_form_class(self):
        return WeaponAddForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        character = get_object_or_404(Character, pk=self.kwargs['pk'])
        # Limit weapons to those not already in the character's inventory
        form.fields['weapon_id'].queryset = Weapon.objects.exclude(inventory_weapons__character=character)
        return form

    def form_valid(self, form):
        character = get_object_or_404(Character, pk=self.kwargs['pk'])
        weapon = form.cleaned_data['weapon_id']
        character.inventory.weapons.add(weapon)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        character = get_object_or_404(Character, pk=self.kwargs['pk'])
        context['character'] = character
        return context

class InventoryRemoveWeaponView(LoginRequiredMixin, FormView):
    template_name = 'juego/inventory_remove_weapon.html'
    success_url = reverse_lazy('juego:characterDetailView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        character = get_object_or_404(Character, pk=self.kwargs['pk'])
        weapon_id = self.kwargs.get('weapon_id')
        weapon = get_object_or_404(Weapon, pk=weapon_id) if weapon_id else None
        context['character'] = character
        context['weapon'] = weapon
        return context

    def form_valid(self, form):
        character = get_object_or_404(Character, pk=self.kwargs['pk'])
        weapon_id = self.kwargs.get('weapon_id')
        if weapon_id:
            try:
                weapon = Weapon.objects.get(pk=weapon_id)
                character.inventory.weapons.remove(weapon)
            except Weapon.DoesNotExist:
                pass  # Silently fail if weapon doesn’t exist
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        # Handle GET request to show the confirmation page
        return super().get(request, *args, **kwargs)



class InventoryAddArmorView(LoginRequiredMixin, FormView):
    template_name = 'juego/inventory_add_armor.html'
    success_url = reverse_lazy('juego:characterDetailView')

    def get_form_class(self):
        return ArmorAddForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        character = get_object_or_404(Character, pk=self.kwargs['pk'])
        # Limit armors to those not already in the character's inventory
        form.fields['armor_id'].queryset = Armor.objects.exclude(inventory_armors__character=character)
        return form

    def form_valid(self, form):
        character = get_object_or_404(Character, pk=self.kwargs['pk'])
        armor = form.cleaned_data['armor_id']
        character.inventory.armors.add(armor)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        character = get_object_or_404(Character, pk=self.kwargs['pk'])
        context['character'] = character
        return context

class InventoryRemoveArmorView(LoginRequiredMixin, FormView):
    template_name = 'juego/inventory_remove_armor.html'
    success_url = reverse_lazy('juego:characterDetailView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        character = get_object_or_404(Character, pk=self.kwargs['pk'])
        armor_id = self.kwargs.get('armor_id')
        armor = get_object_or_404(Armor, pk=armor_id) if armor_id else None
        context['character'] = character
        context['armor'] = armor
        return context

    def form_valid(self, form):
        character = get_object_or_404(Character, pk=self.kwargs['pk'])
        armor_id = self.kwargs.get('armor_id')
        if armor_id:
            try:
                armor = Armor.objects.get(pk=armor_id)
                character.inventory.armors.remove(armor)
            except Armor.DoesNotExist:
                pass  # Silently fail if armor doesn’t exist
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        # Handle GET request to show the confirmation page
        return super().get(request, *args, **kwargs)