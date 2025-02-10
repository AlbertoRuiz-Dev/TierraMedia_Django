# 📜 Nombre del Proyecto

Breve descripción del proyecto.

## 📌 Descripción

Este es un proyecto desarrollado con Django que permite gestionar personajes, sus facciones, inventarios y relaciones. Incluye autenticación, modelos bien estructurados y una interfaz web intuitiva.

## 📌 Características

- ✅ Gestión de usuarios con autenticación
- ✅ *
- ✅ Uso de `LoginRequiredMixin` para proteger vistas
- ✅ Interfaz de usuario construida con **Bootstrap** para una experiencia responsiva y moderna
- ✅ Sistema de inventario y equipamiento

## 📌 Requisitos Previos

Antes de instalar el proyecto, asegúrate de tener:

- Python 3.8...
- Django 4....
- PostgreSQL / SQLite3...
- Git y Virtualenv....

## 📌 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu_usuario/tu_proyecto.git
cd tu_proyecto

# Crear entorno virtual e instalar dependencias
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
pip install -r requirements.txt (Hay que crearlo)

# Configurar la base de datos
python manage.py migrate

# Crear un superusuario
python manage.py createsuperuser

# Ejecutar el servidor
python manage.py runserver
```

## 📌 Uso

1. Accede a `http://127.0.0.1:8000/`
2. Inicia sesión con tu superusuario
3. Gestiona personajes, inventarios y relaciones...

## 📌 Estructura del Proyecto

```bash
📂 tu_proyecto/
├── 📂 juego/  # Aplicación principal
│   ├── 📜 models.py  # Modelos de la base de datos
│   ├── 📜 views.py  # Vistas de la aplicación
│   ├── 📜 urls.py  # Rutas de la aplicación
│   ├── 📜 templates/  # Plantillas HTML
│   └── 📜 tests.py  # Pruebas automatizadas
├── 📂 static/  # Archivos estáticos (CSS, JS, imágenes)
├── 📂 media/  # Archivos subidos por usuarios
├── 📜 manage.py  # Script de gestión de Django
└── 📜 requirements.txt  # Dependencias del proyecto
```

## 📌 URLs del Proyecto

```bash
📂 juego/urls.py
├── /  # Página principal
├── /login/  # Vista de inicio de sesión
├── /logout/  # Vista de cierre de sesión
├── /characters/  # Lista de personajes
├── /character/<int:pk>/  # Detalles de un personaje
├── /inventory/<int:character_id>/  # Detalles del inventario
├── /relationships/  # Lista de relaciones
├── /relationship/<int:pk>/  # Detalles de una relación
├── /create_character/  # Crear un nuevo personaje
└── /create_inventory/<int:character_id>/  # Crear inventario
```

## 📌 Modelos

### `Faction`
- **Campos:**
  - `name`: Nombre de la facción (String)
  - `location`: Ubicación de la facción (String)
- **Descripción:** Representa una facción dentro del sistema, con un nombre y una ubicación específicos.

### `Weapon`
- **Campos:**
  - `name`: Nombre del arma (String)
  - `description`: Descripción del arma (Texto)
  - `damage`: Daño que inflige el arma (Entero)
  - `critic`: Probabilidad de golpe crítico (Flotante)
  - `accuracy`: Precisión del arma (Flotante)
- **Descripción:** Representa un arma en el sistema, con atributos como daño, probabilidad crítica y precisión.

### `Armor`
- **Campos:**
  - `name`: Nombre de la armadura (String)
  - `description`: Descripción de la armadura (Texto)
  - `defense`: Defensa proporcionada por la armadura (Entero)
- **Descripción:** Representa una armadura en el sistema, con un nombre y su valor de defensa.

### `Character`
- **Campos:**
  - `name`: Nombre del personaje (String)
  - `location`: Ubicación del personaje (String)
  - `faction`: Facción a la que pertenece el personaje (Relación con `Faction`)
  - `equipped_weapon`: Arma equipada por el personaje (Relación con `Weapon`)
  - `equipped_armor`: Armadura equipada por el personaje (Relación con `Armor`)
- **Descripción:** Representa un personaje en el sistema, con información sobre su nombre, ubicación, facción, arma y armadura equipadas.

### `Inventory`
- **Campos:**
  - `character`: Personaje al que pertenece el inventario (Relación con `Character`)
  - `weapons`: Armas en el inventario (Relación con `Weapon`)
  - `armors`: Armaduras en el inventario (Relación con `Armor`)
- **Descripción:** Representa el inventario de un personaje, que incluye las armas y armaduras que posee.

### `Relationship`
- **Campos:**
  - `character1`: Primer personaje en la relación (Relación con `Character`)
  - `character2`: Segundo personaje en la relación (Relación con `Character`)
  - `relationship_type`: Tipo de relación entre los dos personajes (String)
- **Descripción:** Representa una relación entre dos personajes, especificando el tipo de relación (por ejemplo, amistad, enemistad). Incluye una validación para evitar relaciones con el mismo personaje

## 📌 Views

### `home` (Página principal)
- **URL:** `/`
- **Descripción:** Esta vista muestra la página de inicio del proyecto. Es la vista de aterrizaje a la que los usuarios accederán al visitar la URL raíz.

### `LoginView` (Iniciar sesión)
- **URL:** `/login/`
- **Descripción:** Esta vista maneja el inicio de sesión de los usuarios. Los usuarios pueden introducir sus credenciales para acceder al sistema.

### `CharacterListView` (Lista de personajes)
- **URL:** `/characters/`
- **Descripción:** Muestra una lista de todos los personajes disponibles en el sistema. Es útil para obtener un vistazo general de los personajes creados en el proyecto.

### `CharacterDetailView` (Detalles de un personaje)
- **URL:** `/character/<int:pk>/`
- **Descripción:** Muestra los detalles completos de un personaje específico basado en su ID. Aquí se incluyen estadísticas, equipo y relaciones de ese personaje.

### `InventoryDetailView` (Detalles del inventario)
- **URL:** `/inventory/<int:character_id>/`
- **Descripción:** Muestra los objetos (armas y armaduras) que un personaje tiene en su inventario. Permite ver qué equipamiento está siendo utilizado por ese personaje.

### `RelationshipListView` (Lista de relaciones)
- **URL:** `/relationships/`
- **Descripción:** Muestra una lista de todas las relaciones entre los personajes en el sistema. Las relaciones pueden ser de amistad, enemistad, etc.

### `RelationshipDetailView` (Detalles de una relación)
- **URL:** `/relationship/<int:pk>/`
- **Descripción:** Muestra los detalles de una relación específica entre dos personajes, como el tipo de relación y la interacción entre ellos.

### `CharacterCreateView` (Crear un personaje)
- **URL:** `/create_character/`
- **Descripción:** Vista para crear un nuevo personaje en el sistema. Permite ingresar el nombre, la facción y otros atributos del personaje.

### `InventoryCreateView` (Crear un inventario)
- **URL:** `/create_inventory/<int:character_id>/`
- **Descripción:** Vista para crear un inventario para un personaje específico. Se asocia con un personaje dado a través del `character_id` en la URL.

## 📌 Pruebas

Ejecuta los tests con:

```bash
python manage.py test....
```

## 📌 Contribución

1. Haz un fork del proyecto
2. Crea una nueva rama (`git checkout -b features/feature_nueva`)
3. Realiza tus cambios y haz commit (`git commit -m 'Añadí una nueva característica'`)
4. Sube los cambios a tu fork (`git push origin features/feature_nueva`)
5. Abre un Pull Request

## 📌 Licencia

Este proyecto está libre de licencia.

## 📌 Contacto

Si tienes preguntas, puedes contactarnos en: elmejorproyecto\@gmail.com



