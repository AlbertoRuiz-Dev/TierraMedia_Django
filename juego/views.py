from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, FormView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from juego.models import *
from juego.forms import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from juego.models import Character
from juego.serializers import CharacterSerializer
import random
from django.shortcuts import render, get_object_or_404
from juego.forms import CharacterBattleForm
import json

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


class BattleView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """Renderiza la página de batalla con el formulario"""
        form = CharacterBattleForm()  # Cargar el formulario de batalla
        return render(request, "juego/battle.html", {'form': form})

    def post(self, request, *args, **kwargs):
        """Procesa los datos del formulario cuando se seleccionan los personajes"""
        form = CharacterBattleForm(request.POST)
        if form.is_valid():
            char1 = form.cleaned_data['character']
            char2 = form.cleaned_data['character2']

            # Establecer el turno de los personajes
            turn_player = char1.id  # Empezamos con el jugador 1

            # Guardar el estado de la batalla en la sesión
            request.session['battle'] = {
                'char1': char1.id,
                'char2': char2.id,
                'char1_hp': 100,
                'char2_hp': 100,
                'turn_player': turn_player,
            }

            # Pasar los personajes seleccionados y el turno al contexto para mostrarlos en la plantilla
            return render(request, "juego/battle.html", {
                'char1': char1,
                'char2': char2,
                'turn_player': turn_player,
            })

        # Si no es válido, devolver el formulario con error
        return render(request, "juego/battle.html",
                      {'form': form, 'error': "Hay un problema con la selección de personajes."})


class AttackView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Obtener los datos enviados por el cliente
            data = json.loads(request.body)
            attacker_id = int(data.get('attacker'))
            ataque_type = data.get('ataque')

            # Verificar que los datos sean correctos
            if not attacker_id or not ataque_type:
                return JsonResponse({'error': 'Datos incompletos'}, status=400)

            # Obtener el estado de la batalla desde la sesión
            battle_state = request.session.get('battle', {})
            if not battle_state:
                return JsonResponse({'error': 'No hay batalla en curso'}, status=400)

            # Obtener IDs de los personajes
            char1_id = battle_state.get('char1')
            char2_id = battle_state.get('char2')

            # Determinar quién es el atacante y quién el defensor
            if attacker_id == char1_id:
                defender_id = char2_id
            elif attacker_id == char2_id:
                defender_id = char1_id
            else:
                return JsonResponse({'error': 'Atacante no válido'}, status=400)

            # Verificar que sea el turno correcto
            if battle_state.get('turn_player') != attacker_id:
                return JsonResponse({'error': 'No es tu turno'}, status=400)

            # Obtener los HP actuales de los personajes
            char1_hp = battle_state.get('char1_hp', 100)
            char2_hp = battle_state.get('char2_hp', 100)

            # Obtener el atacante y el defensor desde la base de datos
            attacker = get_object_or_404(Character, id=attacker_id)
            defender = get_object_or_404(Character, id=defender_id)

            # Determinar el daño según el tipo de ataque
            if ataque_type == 'fuerte':
                damage = attacker.equipped_weapon.damage * 2
            elif ataque_type == 'debil':
                damage = attacker.equipped_weapon.damage
            else:
                return JsonResponse({'error': 'Tipo de ataque inválido'}, status=400)

            # Aplicar el daño al defensor
            if defender_id == char1_id:
                char1_hp -= damage
            else:
                char2_hp -= damage

            # Verificar si la batalla terminó
            if char1_hp <= 0:
                request.session.pop('battle', None)  # Eliminar la batalla de la sesión
                return JsonResponse({'char1_hp': 0, 'char2_hp': char2_hp, 'turn_player': None, 'winner': f'Jugador {char2_id}'})

            if char2_hp <= 0:
                request.session.pop('battle', None)
                return JsonResponse({'char1_hp': char1_hp, 'char2_hp': 0, 'turn_player': None, 'winner': f'Jugador {char1_id}'})

            # Cambiar el turno al otro jugador
            next_turn_player = defender_id

            # Guardar el estado de la batalla actualizado
            request.session['battle'] = {
                'char1': char1_id,
                'char2': char2_id,
                'char1_hp': char1_hp,
                'char2_hp': char2_hp,
                'turn_player': next_turn_player,
            }

            # Devolver la nueva información de la batalla
            return JsonResponse({
                'char1_hp': char1_hp,
                'char1_id': char1_id,
                'char2_hp': char2_hp,
                'char2_id': char2_id,
                'turn_player': next_turn_player,
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class CharacterDetailView(LoginRequiredMixin, DetailView):
    model = Character

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CharacterUpdateView(LoginRequiredMixin, UpdateView):
    model = Character
    form_class = CharacterForm
    template_name = 'juego/character_update.html'
    success_url = reverse_lazy("juego:characterView")

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

