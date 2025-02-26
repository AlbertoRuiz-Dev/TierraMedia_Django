from django.contrib.auth.models import User
from django.db import migrations

from juego.models import *

# Función que elimina todos los datos de la base de datos de la aplicación
def eliminar_datos(apps, schema_editor):
    # Obtener los modelos de la aplicación 'juego' y 'auth'
    Faction = apps.get_model('juego', 'Faction')  # Modelo de Facción
    Weapon = apps.get_model('juego', 'Weapon')  # Modelo de Arma
    Armor = apps.get_model('juego', 'Armor')  # Modelo de Armadura
    Character = apps.get_model('juego', 'Character')  # Modelo de Personaje
    Inventory = apps.get_model('juego', 'Inventory')  # Modelo de Inventario
    Relationship = apps.get_model('juego', 'Relationship')  # Modelo de Relación
    User = apps.get_model('auth', 'User')  # Modelo de Usuario (de la app 'auth')

    # Eliminar las relaciones entre personajes primero para evitar dependencias al borrar personajes
    Relationship.objects.all().delete()
    # Eliminar todos los inventarios
    Inventory.objects.all().delete()
    # Eliminar todos los personajes
    Character.objects.all().delete()
    # Eliminar todas las armas
    Weapon.objects.all().delete()
    # Eliminar todas las armaduras
    Armor.objects.all().delete()
    # Eliminar todas las facciones
    Faction.objects.all().delete()
    # Eliminar los usuarios de prueba y admin
    User.objects.filter(username__in=['prueba', 'admin']).delete()


# Función que pobla la base de datos con datos de prueba
def poblar_datos(apps, schema_editor):
    # Obtener los modelos de la aplicación 'juego'
    Faction = apps.get_model('juego', 'Faction')
    Weapon = apps.get_model('juego', 'Weapon')
    Armor = apps.get_model('juego', 'Armor')
    Character = apps.get_model('juego', 'Character')
    Inventory = apps.get_model('juego', 'Inventory')
    Relationship = apps.get_model('juego', 'Relationship')

    # Crear facciones
    factions = [
        Faction(name="La Hermandad de Acero", location="Fortaleza del Hierro"),
        Faction(name="Los Asesinos Fantasma", location="Ciudad Sombría"),
        Faction(name="Los Renegados del Desierto", location="Tierras Áridas"),
        Faction(name="Los Centinelas del Caos", location="Ruinas Olvidadas")
    ]
    Faction.objects.bulk_create(factions)  # Guardar todas las facciones de una vez

    # Crear armas
    weapons = [
        Weapon(name="Espada del Apocalipsis", description="Una espada legendaria capaz de partir el acero en dos.", damage=75,image="weapons/arma1.jpg"),
        Weapon(name="Rifle de Asalto Fantasma", description="Un rifle silencioso usado por los asesinos más letales.", damage=62,image="weapons/arma2.jpg"),
        Weapon(name="Martillo del Juicio", description="Un martillo pesado que aplasta a los enemigos con furia.", damage=80,image="weapons/arma3.jpg"),
        Weapon(name="Arco del Cazador Nocturno", description="Un arco ligero con flechas que perforan la armadura.", damage=95,image="weapons/arma4.jpg"),
        Weapon(name="Dagas de la Sombra", description="Un par de dagas envenenadas, perfectas para ataques rápidos.", damage=53,image="weapons/arma5.jpg")
    ]
    Weapon.objects.bulk_create(weapons)  # Guardar todas las armas de una vez

    # Crear armaduras
    armors = [
        Armor(name="Armadura del Titán", description="Una armadura pesada que ofrece máxima protección.", defense=15,image="armors/armadura1.jpg"),
        Armor(name="Traje de Sigilo Fantasma", description="Un traje ligero que permite moverse sin ser detectado.", defense=8,image="armors/armadura2.jpg"),
        Armor(name="Coraza del Renegado", description="Una coraza resistente forjada en las arenas del desierto.", defense=12,image="armors/armadura3.jpg"),
        Armor(name="Manto del Caos", description="Un manto que absorbe parte del daño mágico.", defense=10,image="armors/armadura4.jpg"),
        Armor(name="Armadura del Cazador", description="Una armadura flexible que ofrece equilibrio entre defensa y agilidad.", defense=11,image="armors/armadura5.jpg")
    ]
    Armor.objects.bulk_create(armors)  # Guardar todas las armaduras de una vez

    # Obtener referencias a algunas facciones
    faction1 = Faction.objects.get(name="La Hermandad de Acero")
    faction2 = Faction.objects.get(name="Los Asesinos Fantasma")

    # Crear personajes con equipo (arma y armadura)
    characters = [
        Character(
            name="Darius, el Destructor",
            location="Fortaleza del Hierro",
            faction=faction1,
            equipped_weapon=Weapon.objects.get(name="Espada del Apocalipsis"),
            equipped_armor=Armor.objects.get(name="Armadura del Titán"),
            image = "characters/personaje1.jpg"
        ),
        Character(
            name="Nyx, la Sombra",
            location="Ciudad Sombría",
            faction=faction2,
            equipped_weapon=Weapon.objects.get(name="Dagas de la Sombra"),
            equipped_armor=Armor.objects.get(name="Traje de Sigilo Fantasma"),
            image="characters/personaje10.jpg"

        ),
        Character(
            name="Kael, el Martillo",
            location="Tierras Áridas",
            faction=faction1,
            equipped_weapon=Weapon.objects.get(name="Martillo del Juicio"),
            equipped_armor=Armor.objects.get(name="Coraza del Renegado"),
            image="characters/personaje8.jpg"

        ),
        Character(
            name="Selene, la Cazadora",
            location="Ruinas Olvidadas",
            faction=faction2,
            equipped_weapon=Weapon.objects.get(name="Arco del Cazador Nocturno"),
            equipped_armor=Armor.objects.get(name="Armadura del Cazador"),
            image="characters/personaje9.jpg"

        ),
        Character(
            name="Malek, el Caótico",
            location="Ruinas Olvidadas",
            faction=faction1,
            equipped_weapon=Weapon.objects.get(name="Rifle de Asalto Fantasma"),
            equipped_armor=Armor.objects.get(name="Manto del Caos"),
            image="characters/personaje2.jpg"

        )
    ]
    Character.objects.bulk_create(characters)  # Guardar todos los personajes de una vez

    # Crear personajes simples (sin equipo)
    characters_simple = [
        Character(name="Rogar, el Errante", location="Bosques Perdidos",image="characters/personaje3.jpg" ),
        Character(name="Lyra, la Vengadora", location="Ciudad Sombría",image="characters/personaje4.jpg"),
        Character(name="Thalor, el Exiliado", location="Tierras Áridas",image="characters/personaje5.jpg"),
        Character(name="Eryndor, el Hechicero", location="Ruinas Olvidadas",image="characters/personaje6.jpg"),
        Character(name="Astra, la Guardiana", location="Fortaleza del Hierro", image="characters/personaje7.jpg")
    ]
    Character.objects.bulk_create(characters_simple)  # Guardar todos los personajes simples

    # Crear inventarios para TODOS los personajes (con equipo si aplica)
    all_characters = characters + characters_simple
    for character in all_characters:
        inventory = Inventory(character=character)  # Crear el inventario para el personaje
        inventory.save()  # Guardar el inventario
        # Si tiene arma o armadura equipada, añadirlas al inventario
        if character.equipped_weapon:
            inventory.weapons.add(character.equipped_weapon)  # Añadir arma al inventario
        if character.equipped_armor:
            inventory.armors.add(character.equipped_armor)  # Añadir armadura al inventario

    # Crear relaciones entre algunos personajes (amigos, enemigos, etc.)
    relationships = [
        Relationship(character1=characters[0], character2=characters[1], relationship_type='friend'),
        Relationship(character1=characters[1], character2=characters[2], relationship_type='enemy'),
        Relationship(character1=characters[2], character2=characters[3], relationship_type='ally'),
        Relationship(character1=characters[3], character2=characters[4], relationship_type='rival'),
        Relationship(character1=characters[4], character2=characters[0], relationship_type='neutral')
    ]
    Relationship.objects.bulk_create(relationships)  # Guardar todas las relaciones de una vez

    # Creación de usuarios para la administración
    User.objects.create_user(username='prueba', password='prueba')  # Crear un usuario normal
    User.objects.create_superuser(username='admin', email='admin@example.com', password='admin')  # Crear un superusuario

# Migración que ejecuta las funciones de poblar y eliminar datos
class Migration(migrations.Migration):

    # Dependencia de la migración anterior
    dependencies = [
        ('juego', '0005_armor_image_character_image_weapon_image'),
    ]

    # Operaciones que se ejecutan: poblar los datos y definir cómo eliminarlos
    operations = [
        migrations.RunPython(poblar_datos, reverse_code=eliminar_datos),  # Función para poblar y eliminar datos
    ]
