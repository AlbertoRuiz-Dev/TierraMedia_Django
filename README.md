# 📜 Tierra Media

Tierra Media se trata de un proyecto de un juego web creado por: Aarón Gutierrez, Jesús Pérez, Alberto Ruiz, Alejandro Jimenez Perez.


## 📌 Descripción

Este es un proyecto desarrollado con python más Django que permite gestionar personajes, sus facciones, inventarios y relaciones. Incluye autenticación, modelos bien estructurados y una interfaz web intuitiva.

## 📌 Características

- ✅ Gestión de usuarios con autenticación.
- ✅ Gestión de sesiones.
- ✅ Uso de docker.
- ✅ Uso de Postgres:
  - Contiene una migración vacia con una función poblate y otra para revertir el poblate.
- ✅ Uso de `LoginRequiredMixin` para proteger vistas.
- ✅ Uso de Django REST framework:
  - Generación de urls automáticamente con router para las apis.
  - Uso de apis para controlar el CRUD de los modelos.
  - Generación de un gráfico con recuento de personajes por facción.
- ✅ Interfaz de usuario construida con **Bootstrap** para una experiencia responsiva y moderna.
- ✅ Sistema de inventario y equipamiento.
- ✅ Creación de relaciones entre personajes.
- ✅ Funcionalidad CRUD (Crear, Leer, Actualizar y Eliminar) para la gestión de recursos.
- ✅ Interfaz de administración personalizada:
  - Uso del JSONEditorWidget para facilitar la edición de campos JSONField en el panel de administración de Django. Esto permite visualizar y modificar estructuras JSON de forma más amigable e intuitiva.
- ✅ Uso de **optimización de consultas en Django**:  
   - Aplicación de `Q` para realizar consultas complejas.  
   - Uso de `COUNT` para contar elementos de una consulta.  
   - Implementación de `select_related` y `prefetch_related` para optimizar las consultas y evitar problemas de N+1.  
   - Uso de `exclude` para excluir elementos de las consultas.  
   - Aplicación de `annotate` para agregar cálculos y agregaciones a las consultas.

## 📌 Requisitos Previos

Antes de instalar el proyecto, asegúrate de tener un archivo `requirements.txt` con el siguiente contenido:

- Django>=5.0
- psycopg2==2.9.10
- django-extensions
- ipdb
- Pillow
- psycopg2-binary
- django-debug-toolbar
- django-json-widget
- djangorestframework

## 📌 Instalación

```bash
# Clonar el repositorio
git clone git@github.com:AlbertoRuiz-Dev/TierraMedia_Django.git
cd tu_proyecto

# Crear entorno virtual e instalar dependencias
docker compose build
docker compose up -d

# Configurar la base de datos
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# Ejecutar el servidor
docker compose exec web python manage.py runserver
```

## 📌 Uso

1. Accede a `http://127.0.0.1:8000/`
2. Inicia sesión con tu superusuario
3. Gestiona personajes, inventarios y relaciones...

## 📌 Estructura del Proyecto

```bash
📂 nombre_del_proyecto/
│── 📂 juego/               # Aplicación principal
│   ├── 📂 migrations/      # Migraciones de la base de datos
│   ├── 📂 static/          # Archivos estáticos (CSS, JS, imágenes)
│   ├── 📂 templates/       # Plantillas HTML
│   ├── 📂 tests/           # Pruebas automatizadas
│   ├── __init__.py         # Inicialización de la aplicación Django
│   ├── admin.py            # Configuración del panel de administración
│   ├── apps.py             # Configuración de la aplicación
│   ├── forms.py            # Formularios del proyecto
│   ├── models.py           # Modelos de base de datos
│   ├── serializers.py      # Serializadores para API REST
│   ├── urls.py             # Definición de rutas de la aplicación
│   ├── views.py            # Vistas del proyecto
│── 📂 media/               # Archivos multimedia subidos por usuarios
│── 📂 tierramedia/         # Configuración global del proyecto
│   ├── __init__.py         # Inicialización del proyecto Django
│   ├── asgi.py             # Configuración ASGI
│   ├── settings.py         # Configuración de Django
│   ├── urls.py             # Rutas generales del proyecto
│   ├── wsgi.py             # Configuración WSGI
│── .gitignore              # Archivos y carpetas ignoradas en Git
│── docker-compose.yml      # Configuración de Docker Compose
│── Dockerfile              # Configuración para contenedores Docker
│── manage.py               # Script para ejecutar comandos Django
│── README.md               # Documentación principal del proyecto
│── requirements.txt        # Fichero para las instalaciones del proyecto

```

## 📌 URLs del Proyecto

```bash
## 📌 Rutas del Proyecto

A continuación se detallan las principales rutas del proyecto junto con su funcionalidad.

### 🔹 Rutas Generales
- `/` → **IndexView** (Vista principal del índice)

### 🔹 API
- `/api/` → **Router de la API** (Incluye las rutas de la API REST)
- `/api/faction_member_count/` → **get_factions_member_count** (Obtener el conteo de miembros por facción)

### 🔹 Personajes
- `/character/` → **CharacterListView** (Lista de personajes)
- `/character/<int:pk>/` → **CharacterDetailView** (Detalles de un personaje)
- `/character/<int:pk>/update/` → **CharacterUpdateView** (Actualizar un personaje)
- `/character/<int:pk>/delete/` → **CharacterDeleteView** (Eliminar un personaje)
- `/character/create/` → **CharacterCreateView** (Crear un nuevo personaje)

### 🔹 Equipamiento
- `/equipment/` → **EquipmentView** (Vista de equipamiento)
- `/equipment/weapons/` → **WeaponListView** (Lista de armas)
- `/equipment/weapon/<int:pk>/` → **WeaponDetailView** (Detalles de un arma)
- `/equipment/weapons/<int:pk>/edit/` → **WeaponUpdateView** (Editar un arma)
- `/equipment/weapons/<int:pk>/delete/` → **WeaponDeleteView** (Eliminar un arma)
- `/equipment/create_weapon/` → **WeaponCreateView** (Crear un arma nueva)

- `/equipment/armors/` → **ArmorListView** (Lista de armaduras)
- `/equipment/armor/<int:pk>/` → **ArmorDetailView** (Detalles de una armadura)
- `/equipment/armor/<int:pk>/edit/` → **ArmorUpdateView** (Editar una armadura)
- `/equipment/armor/<int:pk>/delete/` → **ArmorDeleteView** (Eliminar una armadura)
- `/equipment/create_armor/` → **ArmorCreateView** (Crear una armadura nueva)

- `/character/<int:pk>/inventory/add_items/` → **InventoryAddItemsView** (Agregar ítems al inventario de un personaje)
- `/character/<int:pk>/equip_weapon/` → **EquipWeaponView** (Equipar un arma a un personaje)
- `/character/<int:pk>/equip_armor/` → **EquipArmorView** (Equipar una armadura a un personaje)

### 🔹 Facciones
- `/faction/` → **FactionView** (Lista de facciones)
- `/faction/list_faction/` → **FactionCharacterFormView** (Formulario de facción)
- `/faction/create/` → **FactionCreateView** (Crear una nueva facción)
- `/faction/delete/<int:pk>/` → **FactionDeleteView** (Eliminar una facción)
- `/faction/detail/<int:pk>/` → **FactionDetailView** (Detalles de una facción)
- `/faction/update/<int:pk>/` → **FactionUpdateView** (Actualizar una facción)

### 🔹 Relaciones entre Personajes
- `/character/relationship/` → **RelationCreateView** (Crear una relación entre personajes)
- `/character/relationship_list/` → **RelationshipListView** (Lista de relaciones)
- `/character/relationship_delete/<int:pk>/` → **RelationshipDeleteView** (Eliminar una relación)
- `/character/relationship_update/<int:pk>/` → **RelationshipUpdateView** (Actualizar una relación)

### 🔹 Batallas
- `/battle/` → **BattleView** (Vista de batallas)
- `/battle/attack/` → **AttackView** (Realizar un ataque en batalla)

### 🔹 Usuarios
- `/accounts/register/` → **RegisterView** (Registro de usuarios)

```

## 📌 Modelos del Proyecto

El proyecto cuenta con varios modelos en Django que representan las entidades principales del juego. A continuación, se describen los modelos y su funcionalidad.

### 🔹 Faction (Facción)
```python
class Faction(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
```
- Representa una **facción** dentro del juego.
- Cada facción tiene un **nombre único** y una **ubicación**.
- Relacionada con los personajes a través del campo **faction** en el modelo `Character`.

### 🔹 Weapon (Arma)
```python
class Weapon(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default="Tan vago como siempre... sin descripción")
    damage = models.IntegerField(default=0)
    critic = models.IntegerField(blank=True, null=True)
    accuracy = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='weapons/', null=True, blank=True, default='weapons/default_weapon.jpg')
```
- Representa un **arma** que los personajes pueden equipar.
- Tiene atributos como **daño, crítico y precisión**.
- Se asignan valores aleatorios a **critic** y **accuracy** si no se especifican.

### 🔹 Armor (Armadura)
```python
class Armor(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default="Tan vago como siempre... sin descripción")
    defense = models.IntegerField(default=0)
    image = models.ImageField(upload_to='armors/', null=True, blank=True, default='armors/default_armor.jpg')
```
- Representa una **armadura** que los personajes pueden equipar.
- Proporciona un **nivel de defensa**.
- Se puede asignar una imagen personalizada o usar la predeterminada.

### 🔹 Character (Personaje)
```python
class Character(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    faction = models.ForeignKey(Faction, on_delete=models.SET_NULL, null=True, blank=True, related_name="members")
    equipped_weapon = models.ForeignKey(Weapon, on_delete=models.SET_NULL, null=True, blank=True, related_name="equipped_weapon")
    equipped_armor = models.ForeignKey(Armor, on_delete=models.SET_NULL, null=True, blank=True, related_name="equipped_armor")
    image = models.ImageField(upload_to='characters/', null=True, blank=True, default='characters/default_character.jpg')
```
- Representa un **personaje jugable o NPC**.
- Puede pertenecer a una **facción** (`Faction`).
- Puede equipar una **arma y armadura** (`Weapon`, `Armor`).
- Se le puede asignar una imagen personalizada.

### 🔹 Inventory (Inventario)
```python
class Inventory(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name="inventory")
    weapons = models.ManyToManyField(Weapon, blank=True, related_name="inventory_weapons")
    armors = models.ManyToManyField(Armor, blank=True, related_name="inventory_armors")
```
- Cada personaje tiene **un único inventario**.
- Puede contener **múltiples armas y armaduras**.
- Relacionado **uno a uno** con `Character`.

### 🔹 Relationship (Relación entre Personajes)
```python
class Relationship(models.Model):
    character1 = models.ForeignKey(Character, related_name='relationships1', on_delete=models.CASCADE)
    character2 = models.ForeignKey(Character, related_name='relationships2', on_delete=models.CASCADE)
    relationship_type = models.CharField(max_length=50, choices=[
        ('friend', 'Amigo'),
        ('enemy', 'Enemigo'),
        ('ally', 'Aliado'),
        ('rival', 'Rival'),
        ('neutral', 'Neutral'),
    ], default='neutral')
```
- Representa la **relación** entre dos personajes.
- Puede ser **amigo, enemigo, aliado, rival o neutral**.
- Se asegura de que un personaje **no pueda tener una relación consigo mismo**.

---

## 📌 Views

# Vistas del Proyecto Django

Este documento describe las vistas basadas en clases utilizadas en el proyecto.

## Vistas Basadas en Clases (Class-Based Views)

### IndexView
```python
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/index.html'
```
**Descripción:** Vista que renderiza la página principal del juego. Solo accesible para usuarios autenticados.

### CharacterView
```python
class CharacterView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/character.html'
```
**Descripción:** Muestra la página de gestión de personajes.

### EquipmentView
```python
class EquipmentView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/equipment.html'
```
**Descripción:** Vista encargada de mostrar la pantalla de equipamiento de los personajes.

### FactionView
```python
class FactionView(LoginRequiredMixin, TemplateView):
    model = Faction
    template_name = 'juego/faction.html'
    context_object_name = 'faction_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        factions = Faction.objects.prefetch_related('members').all()
        context['faction_list'] = factions
        return context
```
## Vista Basada en Función (Function-Based View)

### get_factions_member_count
```python
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
```
**Descripción:** Renderiza la lista de facciones con su información, incluyendo los miembros de cada una.

## ViewSets para API REST

### FactionViewSet
```python
class FactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet que maneja las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    para el modelo Faction. Usa el serializador FactionSerializer.
    """
    queryset = Faction.objects.all().prefetch_related('members')
    serializer_class = FactionSerializer
```

### ArmorViewSet
```python
class ArmorViewSet(viewsets.ModelViewSet):
    """
    ViewSet que maneja las operaciones CRUD para el modelo Armor.
    """
    queryset = Armor.objects.all()
    serializer_class = ArmorSerializer
```

### WeaponViewSet
```python
class WeaponViewSet(viewsets.ModelViewSet):
    """
    ViewSet que maneja las operaciones CRUD para el modelo Weapon.
    """
    queryset = Weapon.objects.all()
    serializer_class = WeaponSerializer
```

### RelationshipViewSet
```python
class RelationshipViewSet(viewsets.ModelViewSet):
    """
    ViewSet que maneja las operaciones CRUD para el modelo Relationship.
    """
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer
```

### InventoryViewSet
```python
class InventoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet que maneja las operaciones CRUD para el modelo Inventory.
    """
    queryset = Inventory.objects.all().prefetch_related('armors', 'weapons')
    serializer_class = InventorySerializer
```

### CharacterViewSet
```python
class CharacterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet que maneja las operaciones de solo lectura para el modelo Character.
    """
    queryset = Character.objects.all().select_related('faction', 'inventory', 'equipped_armor', 'equipped_weapon')
    serializer_class = CharacterSerializerAll
```

### CharacterModifyViewSet
```python
class CharacterModifyViewSet(viewsets.ModelViewSet):
    """
    ViewSet que maneja las operaciones CRUD para el modelo Character.
    """
    queryset = Character.objects.all().select_related('faction', 'inventory', 'equipped_armor', 'equipped_weapon')
    serializer_class = CharacterSerializerModify
```

## Vista de Batalla

### BattleView
```python
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
```
### AttackView
```python
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
```

## Vista de Detalle de Personaje

### CharacterDetailView
```python
class CharacterDetailView(LoginRequiredMixin, DetailView):
    """
    Vista basada en clase para mostrar los detalles de un personaje específico.
    
    Requiere que el usuario esté autenticado y utiliza el modelo `Character`.
    Renderiza la plantilla `character_detail.html`.
    """
    model = Character
    template_name = "juego/character_detail.html"
```

## Vista de Actualización de Personaje

### CharacterUpdateView
```python
class CharacterUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para actualizar la información de un personaje.
    
    Utiliza el formulario `CharacterForm` y restringe la selección de equipo al inventario del personaje.
    """
    model = Character
    form_class = CharacterForm
    template_name = 'juego/character_update.html'
    success_url = reverse_lazy("juego:characterView")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.object and hasattr(self.object, 'inventory'):
            form.fields['equipped_weapon'].queryset = self.object.inventory.weapons.all()
            form.fields['equipped_armor'].queryset = self.object.inventory.armors.all()
            form.fields['equipped_weapon'].empty_label = "Ninguna"
            form.fields['equipped_armor'].empty_label = "Ninguna"
        else:
            form.fields['equipped_weapon'].queryset = Weapon.objects.none()
            form.fields['equipped_armor'].queryset = Armor.objects.none()
        return form
```

## Vista de Lista de Personajes

### CharacterListView
```python
class CharacterListView(LoginRequiredMixin, ListView):
    """
    Vista que muestra una lista de todos los personajes.
    
    Optimiza consultas con `select_related` y `prefetch_related` para mejorar el rendimiento.
    """
    model = Character
    template_name = 'juego/character.html'
    context_object_name = 'character_list'

    def get_queryset(self):
        return Character.objects.select_related(
            'faction', 'equipped_weapon', 'equipped_armor'
        ).prefetch_related(
            'inventory__weapons', 'inventory__armors'
        ).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Personajes'
        return context
```

## Vista de Eliminación de Personaje

### CharacterDeleteView
```python
class CharacterDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vista que permite eliminar un personaje.
    
    Tras la eliminación, redirige a la lista de personajes.
    """
    model = Character
    template_name = 'juego/character_delete.html'
    success_url = reverse_lazy("juego:characterView")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['character_list'] = Character.objects.select_related('faction', 'equipped_weapon', 'equipped_armor').all()
        return context
```
### FactionCharacterFormView
```python
class FactionCharacterFormView(LoginRequiredMixin, FormView):
    """
    Vista que permite seleccionar una facción y mostrar los personajes asociados a ella.
    """
    template_name = 'juego/faction_character_list.html'
    form_class = FactionForm

    def form_valid(self, form):
        faction = form.cleaned_data["faction"]
        characters = Character.objects.select_related('faction').filter(faction=faction)
        return self.render_to_response(self.get_context_data(form=form, characters=characters))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("characters", Character.objects.select_related('faction').all())
        return context
```

## Vista de Personajes por Equipamiento

### EquipmentCharacterFormView
```python
class EquipmentCharacterFormView(LoginRequiredMixin, FormView):
    """
    Vista para filtrar personajes según el arma y/o armadura equipada.
    """
    template_name = 'juego/equipment_character_list.html'
    form_class = EquipmentForm

    def form_valid(self, form):
        weapon = form.cleaned_data["weapon"]
        armor = form.cleaned_data["armor"]
        characters = Character.objects.select_related('equipped_weapon', 'equipped_armor').all()

        if weapon or armor:
            if weapon and armor:
                characters = characters.filter(equipped_weapon=weapon, equipped_armor=armor)
            elif weapon:
                characters = characters.filter(equipped_weapon=weapon)
            elif armor:
                characters = characters.filter(equipped_armor=armor)
        else:
            return self.render_to_response(self.get_context_data(form=form, error_mensaje="No has seleccionado ninguna opción"))

        return self.render_to_response(self.get_context_data(form=form, characters=characters))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("characters", Character.objects.select_related('equipped_weapon', 'equipped_armor').all())
        context.setdefault("weapons", Weapon.objects.all())
        context.setdefault("armors", Armor.objects.all())
        return context
```
## Vista de Creación de Facciones

### FactionCreateView
```python
class FactionCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear una nueva facción.
    """
    model = Faction
    form_class = FactionDefaultForm
    template_name = 'juego/faction_create.html'
    success_url = reverse_lazy("juego:factionView")
```

## Vista de Detalles de Facción

### FactionDetailView
```python
class FactionDetailView(LoginRequiredMixin, DetailView):
    """
    Vista para mostrar los detalles de una facción, incluyendo el número de miembros.
    """
    model = Faction
    template_name = 'juego/faction_detail.html'
    context_object_name = 'faction'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faction = Faction.objects.annotate(member_count=Count('members')).get(id=self.kwargs['pk'])
        context['faction'] = faction
        return context
```

## Vista de Actualización de Facción

### FactionUpdateView
```python
class FactionUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para actualizar los detalles de una facción.
    """
    model = Faction
    form_class = FactionDefaultForm
    template_name = 'juego/faction_update.html'
    success_url = reverse_lazy("juego:factionView")
```

## Vista de Eliminación de Facción

### FactionDeleteView
```python
class FactionDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar una facción.
    """
    model = Faction
    template_name = 'juego/faction_delete.html'
    success_url = reverse_lazy("juego:factionView")
```

## Vista de Creación de Personajes

### CharacterCreateView
```python
class CharacterCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear un nuevo personaje.
    """
    model = Character
    form_class = CharacterForm
    template_name = 'juego/character_create.html'
    success_url = reverse_lazy('juego:characterView')

    def form_valid(self, form):
        self.object = form.save()
        Inventory.objects.create(character=self.object)
        return super().form_valid(form)
```
## Vista de Creación de Facciones

### FactionCreateView
```python
class FactionCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear una nueva facción.
    """
    model = Faction
    form_class = FactionDefaultForm
    template_name = 'juego/faction_create.html'
    success_url = reverse_lazy("juego:factionView")
```

## Vista de Detalles de Facción

### FactionDetailView
```python
class FactionDetailView(LoginRequiredMixin, DetailView):
    """
    Vista para mostrar los detalles de una facción, incluyendo el número de miembros.
    """
    model = Faction
    template_name = 'juego/faction_detail.html'
    context_object_name = 'faction'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faction = Faction.objects.annotate(member_count=Count('members')).get(id=self.kwargs['pk'])
        context['faction'] = faction
        return context
```

## Vista de Actualización de Facción

### FactionUpdateView
```python
class FactionUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para actualizar los detalles de una facción.
    """
    model = Faction
    form_class = FactionDefaultForm
    template_name = 'juego/faction_update.html'
    success_url = reverse_lazy("juego:factionView")
```

## Vista de Eliminación de Facción

### FactionDeleteView
```python
class FactionDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar una facción.
    """
    model = Faction
    template_name = 'juego/faction_delete.html'
    success_url = reverse_lazy("juego:factionView")
```

## Vista de Creación de Personajes

### CharacterCreateView
```python
class CharacterCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear un nuevo personaje.
    """
    model = Character
    form_class = CharacterForm
    template_name = 'juego/character_create.html'
    success_url = reverse_lazy('juego:characterView')

    def form_valid(self, form):
        self.object = form.save()
        Inventory.objects.create(character=self.object)
        return super().form_valid(form)
```

## Vista de Listado de Armas

### WeaponListView
```python
class WeaponListView(LoginRequiredMixin, ListView):
    """
    Vista para mostrar una lista de todas las armas disponibles.
    """
    model = Weapon
    template_name = 'juego/weapon.html'
    context_object_name = 'weapon_list'
```

## Vista de Detalles de Arma

### WeaponDetailView
```python
class WeaponDetailView(LoginRequiredMixin, DetailView):
    """
    Vista para mostrar los detalles de un arma específica.
    """
    model = Weapon
    template_name = 'juego/weapon_detail.html'
    context_object_name = 'weapon'
```

## Vista de Creación de Arma

### WeaponCreateView
```python
class WeaponCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear una nueva arma.
    """
    model = Weapon
    form_class = WeaponForm
    template_name = 'juego/weapon_create.html'
    success_url = reverse_lazy('juego:weaponListView')
```

## Vista de Actualización de Arma

### WeaponUpdateView
```python
class WeaponUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para actualizar los detalles de un arma existente.
    """
    model = Weapon
    form_class = WeaponForm
    template_name = 'juego/weapon_form.html'
    success_url = reverse_lazy('juego:weaponListView')
```

## Vista de Eliminación de Arma

### WeaponDeleteView
```python
class WeaponDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar un arma existente.
    """
    model = Weapon
    template_name = "juego/weapon_delete.html"
    success_url = reverse_lazy('juego:weaponListView')
```

## Vista de Listado de Armaduras

### ArmorListView
```python
class ArmorListView(LoginRequiredMixin, ListView):
    """
    Vista para mostrar una lista de todas las armaduras disponibles.
    """
    model = Armor
    template_name = 'juego/armor.html'
    context_object_name = 'armor_list'
```

## Vista de Detalles de Armadura

### ArmorDetailView
```python
class ArmorDetailView(LoginRequiredMixin, DetailView):
    """
    Vista para mostrar los detalles de una armadura específica.
    """
    model = Armor
    template_name = 'juego/armor_detail.html'
    context_object_name = 'armor'
```

## Vista de Creación de Armadura

### ArmorCreateView
```python
class ArmorCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear una nueva armadura.
    """
    model = Armor
    form_class = ArmorForm
    template_name = 'juego/armor_create.html'
    success_url = reverse_lazy('juego:armorListView')
```

## Vista de Actualización de Armadura

### ArmorUpdateView
```python
class ArmorUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para actualizar los detalles de una armadura existente.
    """
    model = Armor
    form_class = ArmorForm
    template_name = 'juego/armor_form.html'
    success_url = reverse_lazy('juego:armorListView')
```

## Vista de Eliminación de Armadura

### ArmorDeleteView
```python
class ArmorDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar una armadura existente.
    """
    model = Armor
    template_name = "juego/armor_delete.html"
    success_url = reverse_lazy('juego:armorListView')
```
```python
class InventoryAddItemsView(LoginRequiredMixin, FormView):
    """
    Vista para agregar ítems al inventario de un personaje.
    """
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

        selected_weapons = form.cleaned_data['weapons']
        selected_armors = form.cleaned_data['armors']

        current_weapons = set(inventory.weapons.all())
        inventory.weapons.add(*(set(selected_weapons) - current_weapons))
        inventory.weapons.remove(*(current_weapons - set(selected_weapons)))

        current_armors = set(inventory.armors.all())
        inventory.armors.add(*(set(selected_armors) - current_armors))
        inventory.armors.remove(*(current_armors - set(selected_armors)))

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['character'] = get_object_or_404(Character, pk=self.kwargs['pk'])
        return context
```

## Vista de Equipamiento de Arma

### EquipWeaponView
```python
class EquipWeaponView(LoginRequiredMixin, FormView):
    """
    Vista para equipar un arma a un personaje.
    """
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
            inventory.weapons.add(character.equipped_weapon)
        character.equipped_weapon = new_weapon
        character.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['character'] = get_object_or_404(Character, pk=self.kwargs['pk'])
        return context
```
## Vista de Equipamiento de Armadura

### EquipArmorView
```python
class EquipArmorView(LoginRequiredMixin, FormView):
    """
    Vista para equipar una armadura a un personaje.
    """
    template_name = 'juego/equip_armor.html'
    form_class = EquipArmorForm
    success_url = reverse_lazy('juego:characterView')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        character = get_object_or_404(Character, pk=self.kwargs['pk'])
        kwargs['inventory_armors'] = getattr(character.inventory, 'armors', []).all()
        return kwargs

    def form_valid(self, form):
        character = get_object_or_404(Character, pk=self.kwargs['pk'])
        new_armor = form.cleaned_data['armor']
        inventory = getattr(character, 'inventory', Inventory.objects.create(character=character))
        if character.equipped_armor:
            inventory.armors.add(character.equipped_armor)
        character.equipped_armor = new_armor
        character.save()
        return super().form_valid(form)
```
## Vista de Registro de Usuario

### RegisterView
```python
class RegisterView(FormView):
    """
    Vista para registrar un nuevo usuario.
    """
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Inicia sesión automáticamente después del registro
        return super().form_valid(form)
```

## Vista de Lista de Relaciones

### RelationshipListView
```python
class RelationshipListView(LoginRequiredMixin, View):
    """
    Vista para listar y gestionar relaciones entre entidades.
    """
    template_name = 'juego/relationship_list.html'

    def get(self, request, *args, **kwargs):
        relation_list = Relationship.objects.all()
        form = RelationshipForm()
        return render(request, self.template_name, {'relation_list': relation_list, 'form': form})

    def post(self, request, *args, **kwargs):
        relationship_id = request.POST.get("relationship_id")

        if relationship_id:  # Si hay ID, se edita una relación existente
            relationship = get_object_or_404(Relationship, id=relationship_id)
            form = RelationshipForm(request.POST, instance=relationship)
        else:  # Si no hay ID, se crea una nueva relación
            form = RelationshipForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect('juego:relationshipListView')
```

## Vista de Eliminación de Relaciones

### RelationshipDeleteView
```python
class RelationshipDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar una relación existente.
    """
    model = Relationship
    template_name = "juego/relationship_delete.html"
    success_url = reverse_lazy("juego:relationshipListView")
```

## Vista de Actualización de Relaciones

### RelationshipUpdateView
```python
class RelationshipUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para actualizar los detalles de una relación.
    """
    model = Relationship
    template_name = "juego/relationship_update.html"
    success_url = reverse_lazy("juego:relationshipListView")
```



---

Este documento describe las vistas principales del proyecto y su funcionalidad. Para más detalles, consulta el código fuente.



## 📌 Pruebas

Ejecuta los tests con:

```bash
$ docker compose exec web python manage.py test juego/tests/
Found 28 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
............................
----------------------------------------------------------------------
Ran 28 tests in 8.713s

OK
Destroying test database for alias 'default'...

```
## 📌 API
# Documentación de Serializadores en Django REST Framework

Este documento detalla la implementación de los serializadores en Django REST Framework para gestionar personajes, facciones, armas, armaduras e inventarios dentro de un sistema de juego. Se explican las funciones de cada serializador y cómo interactúan con los modelos de Django.

## Tabla de Contenidos
- [Introducción](#introducción)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Serializadores](#serializadores)
  - [WeaponSerializer](#weaponserializer)
  - [ArmorSerializer](#armorserializer)
  - [CharacterMemberSerializer](#charactermemberserializer)
  - [FactionSerializer](#factionserializer)
  - [RelationshipSerializer](#relationshipserializer)
  - [InventorySerializer](#inventoryserializer)
  - [FactionCharacterCountModelSerializer](#factioncharactercountmodelserializer)
  - [InventorySerializerDefault](#inventoryserializerdefault)
  - [CharacterSerializer](#characterserializer)
  - [RelationshipSerializerDefault](#relationshipserializerdefault)
  - [CharacterSerializerAll](#characterserializerall)
  - [CharacterSerializerModify](#characterserializermodify)
- [Vistas](#Vistas)
  - [Obtener número de miembros por facción](#obtener-número-de-miembros-por-facción)
  - [Gestión de facciones](#gestión-de-facciones)
  - [Gestión de armaduras](#gestión-de-armaduras)
  - [Gestión de armas](#gestión-de-armas)
  - [Gestión de relaciones entre personajes](#gestión-de-relaciones-entre-personajes)
  - [Gestión de inventarios](#gestión-de-inventarios)
  - [Gestión de personajes](#gestión-de-personajes)
    - [Solo lectura de personajes](#solo-lectura-de-personajes)
    - [Modificación de personajes](#modificación-de-personajes)

  

---

## Introducción

Los serializadores convierten los modelos de Django en estructuras de datos JSON, facilitando su uso en APIs. En este proyecto, los serializadores permiten gestionar la información de los personajes y sus interacciones en el mundo del juego.

## Requisitos

- Python 3.8+
- Django 4+
- Django REST Framework

## Instalación

Instala Django y Django REST Framework ejecutando:

```sh
pip install django djangorestframework
```

Luego, agrega `'rest_framework'` en `INSTALLED_APPS` dentro del archivo `settings.py`.


```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

## Serializadores

### WeaponSerializer
Este serializador maneja la información de las armas, incluyendo su ID, nombre, daño, crítico, precisión e imagen.

```python
class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = ['id', 'name', 'damage', 'critic', 'accuracy', 'image']
```

### ArmorSerializer
Este serializador maneja la información de las armaduras, incluyendo su ID, nombre, defensa e imagen.

```python
class ArmorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Armor
        fields = ['id', 'name', 'defense', 'image']
```

### CharacterMemberSerializer
Este serializador extrae información básica de los personajes dentro de una facción.

```python
class CharacterMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['id', 'name']
```

### FactionSerializer
Este serializador gestiona la información de las facciones y los personajes asociados a ellas.

```python
class FactionSerializer(serializers.ModelSerializer):
    members = CharacterMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Faction
        fields = ['id', 'name', 'location', 'members']
```

### RelationshipSerializer
Este serializador define y gestiona relaciones entre personajes, asegurando que un personaje no pueda estar relacionado consigo mismo.

```python
class RelationshipSerializer(serializers.ModelSerializer):
    character1 = serializers.PrimaryKeyRelatedField(queryset=Character.objects.all().select_related('faction'))
    character2 = serializers.PrimaryKeyRelatedField(queryset=Character.objects.all().select_related('faction'))

    class Meta:
        model = Relationship
        fields = ['character1', 'character2', 'relationship_type']

    def validate(self, data):
        if data['character1'] == data['character2']:
            raise serializers.ValidationError("Un personaje no puede tener una relación consigo mismo.")
        return data
```

### InventorySerializer
Este serializador maneja el inventario de los personajes, incluyendo armas y armaduras.

```python
class InventorySerializer(serializers.ModelSerializer):
    weapons = serializers.PrimaryKeyRelatedField(queryset=Weapon.objects.all(), many=True)
    armors = serializers.PrimaryKeyRelatedField(queryset=Armor.objects.all(), many=True)
    character = serializers.PrimaryKeyRelatedField(queryset=Character.objects.all().select_related('faction'))

    class Meta:
        model = Inventory
        fields = ['character', 'weapons', 'armors']
```

### FactionCharacterCountModelSerializer
Este serializador devuelve el nombre de una facción y la cantidad de personajes asociados a ella.

```python
class FactionCharacterCountModelSerializer(serializers.ModelSerializer):
    character_count = serializers.SerializerMethodField()

    class Meta:
        model = Faction
        fields = ['name', 'character_count']

    def get_character_count(self, obj):
        return obj.members.count()
```

### CharacterSerializerAll
Este serializador maneja toda la información relevante de un personaje, incluyendo facción, armas, armaduras, relaciones e inventario.

```python
class CharacterSerializerAll(serializers.ModelSerializer):
    faction = FactionSerializer()
    equipped_weapon = WeaponSerializer()
    equipped_armor = ArmorSerializer()
    relationships = serializers.SerializerMethodField()
    inventory = InventorySerializerDefault()

    class Meta:
        model = Character
        fields = ['id', 'name', 'location', 'image', 'faction', 'equipped_weapon', 'equipped_armor', 'relationships', 'inventory']

    def get_relationships(self, obj):
        relationships = Relationship.objects.filter(Q(character1=obj) | Q(character2=obj)).prefetch_related('character1', 'character2')
        return RelationshipSerializerDefault(relationships, many=True).data
```

### CharacterSerializerModify
Este serializador permite modificar detalles de un personaje, como su facción, armas, armaduras e inventario.

```python
class CharacterSerializerModify(serializers.ModelSerializer):
    faction = serializers.PrimaryKeyRelatedField(queryset=Faction.objects.all(), required=False)
    equipped_weapon = serializers.PrimaryKeyRelatedField(queryset=Weapon.objects.all(), required=False)
    equipped_armor = serializers.PrimaryKeyRelatedField(queryset=Armor.objects.all(), required=False)
    inventory = InventorySerializer(required=False)

    class Meta:
        model = Character
        fields = ['id', 'name', 'location', 'image', 'faction', 'equipped_weapon', 'equipped_armor', 'inventory']
```

## Vistas

### Obtener número de miembros por facción

Esta vista maneja una solicitud GET y devuelve un JSON con el nombre de cada facción junto con el número de miembros asociados.

```python
@api_view(['GET'])
def get_factions_member_count(request):
    """
    Obtiene el número de miembros para cada facción registrada en el sistema.
    """
    factions = Faction.objects.all()
    data = [{'name': faction.name, 'member_count': faction.members.count()} for faction in factions]
    return Response(data)
```

### Gestión de facciones

Esta vista permite realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre las facciones.

```python
class FactionViewSet(viewsets.ModelViewSet):
    """
    Proporciona una interfaz para manejar facciones dentro del sistema.
    """
    queryset = Faction.objects.all().prefetch_related('members')
    serializer_class = FactionSerializer
```

### Gestión de armaduras

Esta vista permite gestionar las armaduras dentro del sistema.

```python
class ArmorViewSet(viewsets.ModelViewSet):
    """
    Maneja las operaciones CRUD para el modelo Armor.
    """
    queryset = Armor.objects.all()
    serializer_class = ArmorSerializer
```

### Gestión de armas

Permite gestionar el CRUD de las armas del juego.

```python
class WeaponViewSet(viewsets.ModelViewSet):
    """
    Maneja las operaciones CRUD para el modelo Weapon.
    """
    queryset = Weapon.objects.all()
    serializer_class = WeaponSerializer
```

### Gestión de relaciones entre personajes

Esta vista permite crear, leer, actualizar y eliminar relaciones entre personajes.

```python
class RelationshipViewSet(viewsets.ModelViewSet):
    """
    Maneja las operaciones CRUD para el modelo Relationship.
    """
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer
```

### Gestión de inventarios

Permite la manipulación de inventarios, incluyendo armaduras y armas asociadas a un personaje.

```python
class InventoryViewSet(viewsets.ModelViewSet):
    """
    Maneja las operaciones CRUD para el modelo Inventory.
    """
    queryset = Inventory.objects.all().prefetch_related('armors', 'weapons')
    serializer_class = InventorySerializer
```

### Gestión de personajes

#### Solo lectura de personajes

Esta vista permite obtener información de los personajes sin modificar sus datos.

```python
class CharacterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Maneja la lectura de personajes junto con sus relaciones.
    """
    queryset = Character.objects.all().select_related('faction', 'inventory', 'equipped_armor', 'equipped_weapon')
    serializer_class = CharacterSerializerAll
```

#### Modificación de personajes

Esta vista permite la edición de datos de los personajes, así como su creación y eliminación dentro del sistema.


```python
class CharacterModifyViewSet(viewsets.ModelViewSet):
    """
    Maneja la modificación y edición de personajes en el sistema.
    """
    queryset = Character.objects.all().select_related('faction', 'inventory', 'equipped_armor', 'equipped_weapon')
    serializer_class = CharacterSerializerModify
```



---

## Conclusión
Estos serializadores facilitan la gestión estructurada y eficiente de la información dentro del sistema de juego, asegurando una integración fluida con la API de Django REST Framework. Se pueden modificar y ampliar según las necesidades del proyecto.

## 📌 Contribución

1. Haz un fork del proyecto
2. Crea una nueva rama (`git checkout -b features/feature_nueva`)
3. Realiza tus cambios y haz commit (`git commit -m 'Añadí una nueva característica'`)
4. Sube los cambios a tu fork (`git push origin features/feature_nueva`)
5. Abre un Pull Request

## 📌 Manejo de Errores:
- Explicación de los errores que el programa puede manejar y cómo están gestionados (como la gestión de excepciones para personajes no existentes o equipamiento faltante).
  - Si introduces una relación de un personaje consigo mismo da un mensaje de error.
  - No se puede pegar un personaje que no tenga un arma equipada.

## 📌 Trabajo en Equipo:
- Organización:
  - Hemos usado Discord, Whatsapp, Github y Trello para organizar las tareas.
- Explicación del flujo de trabajo en GitHub.
  - Cada integrante del equipo tiene una rama para cada funcionalidad en un proyecto de GitHub en la cual cada uno hace sus funciones necesarias para sus funciones, una vez se termina el trabajo se sube a la rama correspondiente de GitHub `(commit && push)`. Luego se suben los cambios de la rama al main *(pull requests)* asignando un compañero como reviewer y asi mismo como creador del *pull request*, una vez el compañero revisa el código y crea el pull request `(Squash and merge)`. 
  - Cuando ya tenemos todo en el main, uno de los integrantes se lleva todo a su rama actualizando su main y luego lo pasa a su rama para realizar el archivo global.
  
- Detallar qué partes del código y de la documentación han sido realizadas por cada miembro del equipo. (Engloba HTML, PYTHON, JS, etc...)
  - **Readme:** *Aarón & Jimenez*
  - **Archivo principal (Documentado)**: *Todos*
  - **APIs (Documentado)**: *Aarón*
  - **Personaje (Documentado)**: *Jimenez & Aarón & Alberto*
  - **Equipamiento (Documentado)**: *Alberto*
  - **Armas (Documentado):** *Alberto*
  - **Relaciones (Documentado):** *Jimenez*
  - **Batalla (Documentado):** *Jesús*
  - **Facción (Documentado):** *Aarón*
  - **Listar personajes por facción (Documentado):** *Aarón*
  - **Buscar personajes por equipamiento (Documentado):** *Aarón*
  - **Mostrar todos los personajes (Documentado):** *Aarón & Alberto*
 
## 📌 Licencia

Este proyecto está libre de licencia.

## 📌 Contacto

Si tienes preguntas, puedes contactarnos en: muerteajavascript@gmail.com


