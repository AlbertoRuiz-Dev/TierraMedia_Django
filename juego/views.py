from django.contrib.auth import login
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
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
from rest_framework import status, viewsets
from juego.serializers import *
import random
from django.shortcuts import render, get_object_or_404
from juego.forms import CharacterBattleForm
import json
from django.contrib.auth import login
from django.db.models import Count
from django.http import JsonResponse
from django.views import View

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


# Vista para obtener el conteo de miembros por facción
@api_view(['GET'])  # Especificamos que esta vista solo responde a solicitudes GET
def get_factions_member_count(request):
    """
    Esta vista obtiene el número de miembros para cada facción en el sistema.

    Procesa una solicitud GET y devuelve un JSON con el nombre de la facción
    y su respectivo número de miembros.
    """
    # Obtener todas las facciones desde la base de datos
    factions = Faction.objects.all()

    # Inicializar una lista vacía para almacenar los datos que se devolverán
    data = []

    # Recorrer cada facción
    for faction in factions:
        # Contar el número de miembros asociados a cada facción
        member_count = faction.members.count()

        # Añadir los datos de la facción y el conteo de miembros a la lista
        data.append({
            'name': faction.name,  # Nombre de la facción
            'member_count': member_count  # Número de miembros
        })

    # Retornar la respuesta con los datos en formato JSON
    return Response(data)


# Vista para gestionar las facciones usando el viewset
class FactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet que maneja las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    para el modelo Faction. Usa el serializador FactionSerializer.
    """
    # Definir la consulta que se usará para obtener los objetos de Faction
    queryset = Faction.objects.all().prefetch_related(
        'members')  # Usamos prefetch_related para optimizar la consulta de miembros
    # Especificar el serializador que se utilizará para convertir los objetos de Faction a JSON
    serializer_class = FactionSerializer


# Vista para gestionar las armaduras usando el viewset
class ArmorViewSet(viewsets.ModelViewSet):
    """
    ViewSet que maneja las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    para el modelo Armor. Usa el serializador ArmorSerializer.
    """
    # Definir la consulta que se usará para obtener los objetos de Armor
    queryset = Armor.objects.all()  # Obtener todos los objetos de Armor
    # Especificar el serializador que se utilizará para convertir los objetos de Armor a JSON
    serializer_class = ArmorSerializer


# Vista para gestionar las armas usando el viewset
class WeaponViewSet(viewsets.ModelViewSet):
    """
    ViewSet que maneja las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    para el modelo Weapon. Usa el serializador WeaponSerializer.
    """
    # Definir la consulta que se usará para obtener los objetos de Weapon
    queryset = Weapon.objects.all()  # Obtener todos los objetos de Weapon
    # Especificar el serializador que se utilizará para convertir los objetos de Weapon a JSON
    serializer_class = WeaponSerializer


# Vista para gestionar las relaciones entre personajes usando el viewset
class RelationshipViewSet(viewsets.ModelViewSet):
    """
    ViewSet que maneja las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    para el modelo Relationship. Usa el serializador RelationshipSerializer.
    """
    # Definir la consulta que se usará para obtener los objetos de Relationship
    queryset = Relationship.objects.all()  # Obtener todas las relaciones entre personajes
    # Especificar el serializador que se utilizará para convertir los objetos de Relationship a JSON
    serializer_class = RelationshipSerializer


# Vista para gestionar los inventarios de personajes usando el viewset
class InventoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet que maneja las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    para el modelo Inventory. Usa el serializador InventorySerializer.
    """
    # Definir la consulta que se usará para obtener los objetos de Inventory
    queryset = Inventory.objects.all().prefetch_related('armors',
                                                        'weapons')  # Usamos prefetch_related para optimizar la consulta de armaduras y armas
    # Especificar el serializador que se utilizará para convertir los objetos de Inventory a JSON
    serializer_class = InventorySerializer


# Vista para gestionar los personajes usando el viewset
class CharacterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet que maneja las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    para el modelo Character. Usa el serializador CharacterSerializer.
    """
    # Definir la consulta que se usará para obtener los objetos de Character
    queryset = Character.objects.all().select_related('faction', 'inventory', 'equipped_armor',
                                                      'equipped_weapon')  # Usamos select_related para optimizar la consulta de relaciones
    # Especificar el serializador que se utilizará para convertir los objetos de Character a JSON
    serializer_class = CharacterSerializerAll


# Vista para gestionar los personajes usando el viewset
class CharacterModifyViewSet(viewsets.ModelViewSet):
    """
    ViewSet que maneja las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    para el modelo Character. Usa el serializador CharacterSerializer.
    """
    # Definir la consulta que se usará para obtener los objetos de Character
    queryset = Character.objects.all().select_related('faction', 'inventory', 'equipped_armor',
                                                      'equipped_weapon')  # Usamos select_related para optimizar la consulta de relaciones
    # Especificar el serializador que se utilizará para convertir los objetos de Character a JSON
    serializer_class = CharacterSerializerModify


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

            # Obtener los personajes para estadísticas
            character1 = Character.objects.select_related('equipped_armor', 'equipped_weapon').get(id=char1_id)
            character2 = Character.objects.select_related('equipped_armor', 'equipped_weapon').get(id=char2_id)

            # Obtener las estadísticas que se necesitarán
            character1_accuracy = character1.equipped_weapon.accuracy if character1.equipped_weapon.accuracy else 50
            character2_accuracy = character2.equipped_weapon.accuracy if character2.equipped_weapon.accuracy else 50
            character1_critic = character1.equipped_weapon.critic if character1.equipped_weapon.critic else 10
            character2_critic = character2.equipped_weapon.critic if character2.equipped_weapon.critic else 10
            character1_defense = character1.equipped_armor.defense if character1.equipped_armor.defense else 0
            character2_defense = character2.equipped_armor.defense if character2.equipped_armor.defense else 0

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
                damage = attacker.equipped_weapon.damage * 1.5
            elif ataque_type == 'debil':
                damage = attacker.equipped_weapon.damage
            else:
                return JsonResponse({'error': 'Tipo de ataque inválido'}, status=400)

            # Aplicar el daño al defensor
            if defender_id == char1_id:
                accuracy = random.randint(0, 100) <= character2_accuracy
                critic = random.randint(0, 100) <= character2_critic
                damage = damage * 2 if critic else damage
                damage = damage - character1_defense if damage > character1_defense else 0
                damage = damage if accuracy else 0
                char1_hp -= damage
            else:
                accuracy = random.randint(0, 100) <= character1_accuracy
                critic = random.randint(0, 100) <= character1_critic
                damage = damage * 2 if critic else damage
                damage = damage - character2_defense if damage > character2_defense else 0
                damage = damage if accuracy else 0
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
    """
    Vista basada en clase para mostrar los detalles de un personaje específico.

    Esta vista muestra la información detallada de un personaje. Requiere que el usuario
    esté autenticado para acceder a la página (gracias a LoginRequiredMixin).
    Utiliza el modelo `Character` y renderiza el template `character_detail.html`.
    """

    # Especifica el modelo que se utilizará para esta vista, en este caso `Character`
    model = Character

    # Especifica la ubicación del template que se utilizará para renderizar la vista
    template_name = "juego/character_detail.html"


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
    """
    Vista que permite seleccionar una facción y mostrar los personajes asociados a ella.

    Se utiliza un formulario (`FactionForm`) para que el usuario elija una facción.
    Los personajes que pertenecen a la facción seleccionada se muestran en la página.
    """

    # Especifica el template que se usará para renderizar la vista
    template_name = 'juego/faction_character_list.html'

    # Especifica el formulario que se usará en esta vista
    form_class = FactionForm

    def form_valid(self, form):
        """
        Método que se llama cuando el formulario es válido.

        Filtra los personajes según la facción seleccionada en el formulario
        y los pasa al contexto para ser renderizados en la plantilla.
        """
        faction = form.cleaned_data["faction"]  # Obtiene la facción seleccionada
        characters = Character.objects.select_related('faction').filter(
            faction=faction)  # Filtra personajes por facción
        return self.render_to_response(self.get_context_data(form=form, characters=characters))

    def get_context_data(self, **kwargs):
        """
        Añade información adicional al contexto de la vista.

        Si no se ha seleccionado una facción, muestra todos los personajes por defecto.
        """
        context = super().get_context_data(**kwargs)
        context.setdefault("characters", Character.objects.select_related(
            'faction').all())  # Mostrar todos los personajes por defecto
        return context


class EquipmentCharacterFormView(LoginRequiredMixin, FormView):
    """
    Vista para filtrar personajes según el arma y/o armadura equipada.

    Permite al usuario seleccionar un arma y/o armadura y mostrar los personajes que
    tienen esas opciones equipadas.
    """

    # Especifica el template que se usará para renderizar la vista
    template_name = 'juego/equipment_character_list.html'

    # Especifica el formulario que se usará en esta vista
    form_class = EquipmentForm

    def form_valid(self, form):
        """
        Método que se llama cuando el formulario es válido.

        Filtra los personajes según el arma y la armadura seleccionadas.
        Si se selecciona un arma y una armadura, muestra los personajes que tienen ambas equipadas.
        """
        weapon = form.cleaned_data["weapon"]  # Obtiene el arma seleccionada
        armor = form.cleaned_data["armor"]  # Obtiene la armadura seleccionada
        characters = Character.objects.select_related('equipped_weapon', 'equipped_armor').all()

        # Filtra según las selecciones del formulario
        if weapon or armor:
            if weapon and armor:
                characters = characters.filter(equipped_weapon=weapon, equipped_armor=armor).select_related(
                    'equipped_weapon', 'equipped_armor').all()  # Filtros combinados
            elif weapon:
                characters = characters.filter(equipped_weapon=weapon).select_related('equipped_weapon',
                                                                                      'equipped_armor').all()  # Filtra personajes por arma
            elif armor:
                characters = characters.filter(equipped_armor=armor).select_related('equipped_weapon',
                                                                                    'equipped_armor').all()  # Filtra personajes por armadura
        else:
            return self.render_to_response(
                self.get_context_data(form=form,
                                      error_mensaje="No has seleccionado ningúna opción"))  # Si no hay selección, muestra un mensaje de error

        # Renderiza la respuesta con los personajes filtrados
        return self.render_to_response(self.get_context_data(form=form, characters=characters))

    def get_context_data(self, **kwargs):
        """
        Añade información adicional al contexto de la vista.

        Incluye todos los personajes, armas y armaduras disponibles por defecto.
        """
        context = super().get_context_data(**kwargs)
        context.setdefault("characters", Character.objects.select_related('equipped_weapon',
                                                                          'equipped_armor').all())  # Mostrar todos los personajes por defecto
        context.setdefault("weapons", Weapon.objects.all())  # Mostrar todas las armas por defecto
        context.setdefault("armors", Armor.objects.all())  # Mostrar todas las armaduras por defecto
        return context


class RelationCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear una nueva relación entre personajes.

    Utiliza un formulario de creación para generar una relación entre dos personajes,
    especificando el tipo de relación.
    """

    model = Relationship  # Especifica el modelo relacionado
    fields = ['', '']  # Define los campos del formulario
    template_name = ''  # Especifica el template que se usará
    success_url = ''  # Define la URL a la que se redirigirá al usuario tras una creación exitosa


class FactionCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear una nueva facción.

    Utiliza un formulario de creación (`FactionDefaultForm`) para que el usuario
    pueda crear una nueva facción.
    """

    model = Faction  # Especifica el modelo relacionado
    form_class = FactionDefaultForm  # Usamos el formulario `FactionDefaultForm`
    template_name = 'juego/faction_create.html'  # Especifica el template para renderizar la vista
    success_url = reverse_lazy("juego:factionView")  # Redirige a la vista de la facción después de crearla


class FactionDetailView(LoginRequiredMixin, DetailView):
    """
    Vista para mostrar los detalles de una facción, incluyendo el número de miembros.

    Muestra la información detallada de una facción y cuenta cuántos miembros tiene.
    """

    model = Faction  # Especifica el modelo relacionado
    template_name = 'juego/faction_detail.html'  # Especifica el template para renderizar la vista
    context_object_name = 'faction'  # Nombre del objeto que se pasará al contexto

    def get_context_data(self, **kwargs):
        """
        Añade el conteo de miembros de la facción al contexto.

        Obtiene la facción por su ID, agrega el conteo de miembros y lo pasa al contexto.
        """
        context = super().get_context_data(**kwargs)
        faction = Faction.objects.annotate(member_count=Count('members')).get(
            id=self.kwargs['pk'])  # Obtiene la facción con el conteo de miembros
        context['faction'] = faction  # Agrega la facción al contexto
        return context


class FactionUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para actualizar los detalles de una facción.

    Permite modificar los detalles de una facción existente.
    """

    model = Faction  # Especifica el modelo relacionado
    form_class = FactionDefaultForm  # Usamos el formulario `FactionDefaultForm`
    template_name = 'juego/faction_update.html'  # Especifica el template para renderizar la vista
    success_url = reverse_lazy("juego:factionView")  # Redirige a la vista de facción después de actualizarla


class FactionDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar una facción.

    Permite eliminar una facción existente.
    """

    model = Faction  # Especifica el modelo relacionado
    template_name = 'juego/faction_delete.html'  # Especifica el template para renderizar la vista
    success_url = reverse_lazy("juego:factionView")  # Redirige a la vista de facción después de eliminarla


class CharacterCreateView(LoginRequiredMixin, CreateView):
    model = Character
    form_class = CharacterForm
    template_name = 'juego/character_create.html'
    success_url = reverse_lazy('juego:characterView')

    def form_valid(self, form):
        self.object = form.save()
        Inventory.objects.create(character=self.object)
        return super().form_valid(form)

class WeaponListView(LoginRequiredMixin, ListView):
    model = Weapon
    template_name = 'juego/weapon.html'
    context_object_name = 'weapon_list'

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
    context_object_name = 'armor_list'


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

class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class RelationshipListView(LoginRequiredMixin, View):  # Cambiamos a View para manejar GET y POST
    template_name = 'juego/relationship_list.html'

    def get(self, request, *args, **kwargs):
        relation_list = Relationship.objects.all()
        form = RelationshipForm()
        return render(request, self.template_name, {'relation_list': relation_list, 'form': form})

    def post(self, request, *args, **kwargs):
        relationship_id = request.POST.get("relationship_id")

        if relationship_id:  # Si hay ID, estamos editando una relación existente
            relationship = get_object_or_404(Relationship, id=relationship_id)
            form = RelationshipForm(request.POST, instance=relationship)
        else:  # Si no hay ID, creamos una nueva relación
            form = RelationshipForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect('juego:relationshipListView')

class RelationshipDeleteView(LoginRequiredMixin, DeleteView):
    model = Relationship
    template_name = "juego/relationship_delete.html"
    success_url = reverse_lazy("juego:relationshipListView")

class RelationshipUpdateView(LoginRequiredMixin, UpdateView):
    model = Relationship
    template_name = "juego/relationship_update.html"
    success_url = reverse_lazy("juego:relationshipListView")