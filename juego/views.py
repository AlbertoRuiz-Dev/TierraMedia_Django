from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, FormView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from juego.models import *
from juego.forms import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import viewsets

from juego.models import Character
from juego.serializers import *

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
    model = Faction
    template_name = 'juego/faction.html'
    context_object_name = 'faction_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        factions = Faction.objects.prefetch_related('members').all()
        context['faction_list'] = factions
        return context

@api_view(['GET'])
def get_factions_member_count(request):
    factions = Faction.objects.all()
    data = []

    for faction in factions:
        member_count = faction.members.count()  # Cuenta el número de miembros
        data.append({
            'name': faction.name,
            'member_count': member_count
        })

    return Response(data)

class FactionViewSet(viewsets.ModelViewSet):
    queryset = Faction.objects.all().prefetch_related('members')
    serializer_class = FactionSerializer

class ArmorViewSet(viewsets.ModelViewSet):
    queryset = Armor.objects.all()  # Todos los objetos de Armor
    serializer_class = ArmorSerializer  # Usa el ArmorSerializer para la serialización

class WeaponViewSet(viewsets.ModelViewSet):
    queryset = Weapon.objects.all()  # Obtiene todos los objetos de Weapon
    serializer_class = WeaponSerializer  # Usa el WeaponSerializer para la serialización

class RelationshipViewSet(viewsets.ModelViewSet):
    queryset = Relationship.objects.all()  # Obtiene todas las relaciones
    serializer_class = RelationshipSerializer  # Usa el RelationshipSerializer para la serialización

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all().prefetch_related('armors', 'weapons')
    serializer_class = InventorySerializer

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all().select_related('faction', 'inventory', 'equipped_armor', 'equipped_weapon')
    serializer_class = CharacterSerializer

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
            # Limitar equipped_weapon y equipped_armor al inventario del personaje
            form.fields['equipped_weapon'].queryset = self.object.inventory.weapons.all()
            form.fields['equipped_armor'].queryset = self.object.inventory.armors.all()
            # Permitir "Ninguna" como opción
            form.fields['equipped_weapon'].empty_label = "Ninguna"
            form.fields['equipped_armor'].empty_label = "Ninguna"
        else:
            # Si no hay inventario, no permitir selección
            form.fields['equipped_weapon'].queryset = Weapon.objects.none()
            form.fields['equipped_armor'].queryset = Armor.objects.none()
        return form

class CharacterListView(LoginRequiredMixin, ListView):
    model = Character
    template_name = 'juego/character.html'
    context_object_name = 'character_list'

    def get_queryset(self):
        # Optimizamos la consulta con select_related y prefetch_related
        return Character.objects.select_related(
            'faction', 'equipped_weapon', 'equipped_armor'
        ).prefetch_related(
            'inventory__weapons', 'inventory__armors'
        ).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadimos datos adicionales si es necesario
        context['title'] = 'Lista de Personajes'
        return context


class CharacterDeleteView(LoginRequiredMixin, DeleteView):
    model = Character
    template_name = 'juego/character_delete.html'
    success_url = reverse_lazy("juego:characterView")

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
        characters = Character.objects.select_related('equipped_weapon', 'equipped_armor').all()

        if weapon or armor:
            if weapon and armor:
                characters = characters.filter(equipped_weapon=weapon, equipped_armor=armor).select_related('equipped_weapon', 'equipped_armor').all()  # Filtros combinados
            elif weapon:
                characters = characters.filter(equipped_weapon=weapon).select_related('equipped_weapon', 'equipped_armor').all()  # Filtra personajes por arma
            elif armor:
                characters = characters.filter(equipped_armor=armor).select_related('equipped_weapon', 'equipped_armor').all()  # Filtra personajes por armadura
        else:
            return self.render_to_response(
                (self.get_context_data(form=form, error_mensaje="No has seleccionado ningúna opción")))

        return self.render_to_response(self.get_context_data(form=form, characters=characters))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("characters", Character.objects.select_related('equipped_weapon', 'equipped_armor').all())  # Mostrar todos los personajes por defecto
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

class FactionDetailView(LoginRequiredMixin, DetailView):
    # FALTAN TEST DE ESTA CLASE

    model = Faction
    template_name = 'juego/faction_detail.html'
    context_object_name = 'faction'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faction = Faction.objects.annotate(member_count=Count('members')).get(id=self.kwargs['pk'])
        context['faction'] = faction
        return context

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
    success_url = reverse_lazy('juego:characterView')

    def form_valid(self, form):
        self.object = form.save()
        Inventory.objects.create(character=self.object)
        return super().form_valid(form)

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

class InventoryAddItemsView(LoginRequiredMixin, FormView):
    template_name = 'juego/inventory_add_items.html'
    form_class = InventoryAddItemsForm
    success_url = reverse_lazy('juego:characterView')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        character = get_object_or_404(Character, pk=self.kwargs['pk'])
        kwargs['character'] = character
        return kwargs

    def form_valid(self, form):
        character = get_object_or_404(Character, pk=self.kwargs['pk'])
        try:
            inventory = character.inventory
        except Character.inventory.RelatedObjectDoesNotExist:
            inventory = Inventory.objects.create(character=character)

        # Obtener los ítems seleccionados en el formulario
        selected_weapons = form.cleaned_data['weapons']
        selected_armors = form.cleaned_data['armors']

        # Añadir o eliminar armas del inventario
        current_weapons = set(inventory.weapons.all())
        weapons_to_add = set(selected_weapons) - current_weapons
        weapons_to_remove = current_weapons - set(selected_weapons)
        inventory.weapons.add(*weapons_to_add)
        inventory.weapons.remove(*weapons_to_remove)

        # Añadir o eliminar armaduras del inventario
        current_armors = set(inventory.armors.all())
        armors_to_add = set(selected_armors) - current_armors
        armors_to_remove = current_armors - set(selected_armors)
        inventory.armors.add(*armors_to_add)
        inventory.armors.remove(*armors_to_remove)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['character'] = get_object_or_404(Character, pk=self.kwargs['pk'])
        return context

class EquipWeaponView(LoginRequiredMixin, FormView):
    template_name = 'juego/equip_weapon.html'
    form_class = EquipWeaponForm
    success_url = reverse_lazy('juego:characterView')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        character = get_object_or_404(Character, pk=self.kwargs['pk'])
        try:
            inventory = character.inventory
            kwargs['inventory_weapons'] = inventory.weapons.all()
        except Character.inventory.RelatedObjectDoesNotExist:
            kwargs['inventory_weapons'] = []
        return kwargs

    def form_valid(self, form):
        character = get_object_or_404(Character, pk=self.kwargs['pk'])
        new_weapon = form.cleaned_data['weapon']
        try:
            inventory = character.inventory
        except Character.inventory.RelatedObjectDoesNotExist:
            inventory = Inventory.objects.create(character=character)
        if character.equipped_weapon:
            inventory.weapons.add(character.equipped_weapon)  # Añadir el arma equipada actual al inventario
        character.equipped_weapon = new_weapon
        character.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['character'] = get_object_or_404(Character, pk=self.kwargs['pk'])
        return context

class EquipArmorView(LoginRequiredMixin, FormView):
    template_name = 'juego/equip_armor.html'
    form_class = EquipArmorForm
    success_url = reverse_lazy('juego:characterView')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        character = get_object_or_404(Character, pk=self.kwargs['pk'])
        try:
            inventory = character.inventory
            kwargs['inventory_armors'] = inventory.armors.all()
        except Character.inventory.RelatedObjectDoesNotExist:
            kwargs['inventory_armors'] = []
        return kwargs

    def form_valid(self, form):
        character = get_object_or_404(Character, pk=self.kwargs['pk'])
        new_armor = form.cleaned_data['armor']
        try:
            inventory = character.inventory
        except Character.inventory.RelatedObjectDoesNotExist:
            inventory = Inventory.objects.create(character=character)
        if character.equipped_armor:
            inventory.armors.add(character.equipped_armor)  # Añadir la armadura equipada actual al inventario
        character.equipped_armor = new_armor
        character.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['character'] = get_object_or_404(Character, pk=self.kwargs['pk'])
        return context