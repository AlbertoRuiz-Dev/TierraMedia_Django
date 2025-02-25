from django.contrib.auth.models import User
from django.db import migrations

from juego.models import *

def eliminar_datos(apps, schema_editor):
    # Obtener los modelos
    Faction = apps.get_model('juego', 'Faction')
    Weapon = apps.get_model('juego', 'Weapon')
    Armor = apps.get_model('juego', 'Armor')
    Character = apps.get_model('juego', 'Character')
    Inventory = apps.get_model('juego', 'Inventory')
    Relationship = apps.get_model('juego', 'Relationship')
    User = apps.get_model('auth', 'User')

    # Eliminar relaciones primero para evitar dependencias
    Relationship.objects.all().delete()
    Inventory.objects.all().delete()
    Character.objects.all().delete()
    Weapon.objects.all().delete()
    Armor.objects.all().delete()
    Faction.objects.all().delete()
    User.objects.filter(username__in=['prueba', 'admin']).delete()

def poblar_datos(apps, schema_editor):
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
    Faction.objects.bulk_create(factions)

    # Crear armas
    weapons = [
        Weapon(name="Espada del Apocalipsis", description="Una espada legendaria capaz de partir el acero en dos.", damage=75),
        Weapon(name="Rifle de Asalto Fantasma", description="Un rifle silencioso usado por los asesinos más letales.", damage=62),
        Weapon(name="Martillo del Juicio", description="Un martillo pesado que aplasta a los enemigos con furia.", damage=80),
        Weapon(name="Arco del Cazador Nocturno", description="Un arco ligero con flechas que perforan la armadura.", damage=95),
        Weapon(name="Dagas de la Sombra", description="Un par de dagas envenenadas, perfectas para ataques rápidos.", damage=53)
    ]
    Weapon.objects.bulk_create(weapons)

    # Crear armaduras
    armors = [
        Armor(name="Armadura del Titán", description="Una armadura pesada que ofrece máxima protección.", defense=15),
        Armor(name="Traje de Sigilo Fantasma", description="Un traje ligero que permite moverse sin ser detectado.", defense=8),
        Armor(name="Coraza del Renegado", description="Una coraza resistente forjada en las arenas del desierto.", defense=12),
        Armor(name="Manto del Caos", description="Un manto que absorbe parte del daño mágico.", defense=10),
        Armor(name="Armadura del Cazador", description="Una armadura flexible que ofrece equilibrio entre defensa y agilidad.", defense=11)
    ]
    Armor.objects.bulk_create(armors)

    # Obtener referencias a facciones
    faction1 = Faction.objects.get(name="La Hermandad de Acero")
    faction2 = Faction.objects.get(name="Los Asesinos Fantasma")

    # Crear personajes con equipo
    characters = [
        Character(
            name="Darius, el Destructor",
            location="Fortaleza del Hierro",
            faction=faction1,
            equipped_weapon=Weapon.objects.get(name="Espada del Apocalipsis"),
            equipped_armor=Armor.objects.get(name="Armadura del Titán")
        ),
        Character(
            name="Nyx, la Sombra",
            location="Ciudad Sombría",
            faction=faction2,
            equipped_weapon=Weapon.objects.get(name="Dagas de la Sombra"),
            equipped_armor=Armor.objects.get(name="Traje de Sigilo Fantasma")
        ),
        Character(
            name="Kael, el Martillo",
            location="Tierras Áridas",
            faction=faction1,
            equipped_weapon=Weapon.objects.get(name="Martillo del Juicio"),
            equipped_armor=Armor.objects.get(name="Coraza del Renegado")
        ),
        Character(
            name="Selene, la Cazadora",
            location="Ruinas Olvidadas",
            faction=faction2,
            equipped_weapon=Weapon.objects.get(name="Arco del Cazador Nocturno"),
            equipped_armor=Armor.objects.get(name="Armadura del Cazador")
        ),
        Character(
            name="Malek, el Caótico",
            location="Ruinas Olvidadas",
            faction=faction1,
            equipped_weapon=Weapon.objects.get(name="Rifle de Asalto Fantasma"),
            equipped_armor=Armor.objects.get(name="Manto del Caos")
        )
    ]
    Character.objects.bulk_create(characters)

    # Crear personajes simples
    characters_simple = [
        Character(name="Rogar, el Errante", location="Bosques Perdidos"),
        Character(name="Lyra, la Vengadora", location="Ciudad Sombría"),
        Character(name="Thalor, el Exiliado", location="Tierras Áridas"),
        Character(name="Eryndor, el Hechicero", location="Ruinas Olvidadas"),
        Character(name="Astra, la Guardiana", location="Fortaleza del Hierro")
    ]
    Character.objects.bulk_create(characters_simple)

    # Crear inventarios para TODOS los personajes (characters + characters_simple)
    all_characters = characters + characters_simple
    for character in all_characters:
        inventory = Inventory(character=character)
        inventory.save()
        # Si tiene arma o armadura equipada, añadirlas al inventario
        if character.equipped_weapon:
            inventory.weapons.add(character.equipped_weapon)
        if character.equipped_armor:
            inventory.armors.add(character.equipped_armor)

    # Crear relaciones entre personajes
    relationships = [
        Relationship(character1=characters[0], character2=characters[1], relationship_type='friend'),
        Relationship(character1=characters[1], character2=characters[2], relationship_type='enemy'),
        Relationship(character1=characters[2], character2=characters[3], relationship_type='ally'),
        Relationship(character1=characters[3], character2=characters[4], relationship_type='rival'),
        Relationship(character1=characters[4], character2=characters[0], relationship_type='neutral')
    ]
    Relationship.objects.bulk_create(relationships)

    # Creación de usuarios
    User.objects.create_user(username='prueba', password='prueba')
    User.objects.create_superuser(username='admin', email='admin@example.com', password='admin')

class Migration(migrations.Migration):

    dependencies = [
        ('juego', '0005_armor_image_character_image_weapon_image'),
    ]

    operations = [
        migrations.RunPython(poblar_datos, reverse_code=eliminar_datos),
    ]