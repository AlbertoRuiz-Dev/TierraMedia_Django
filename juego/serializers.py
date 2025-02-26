from rest_framework import serializers
from .models import *
from django.db.models import Q


class WeaponSerializer(serializers.ModelSerializer):
    """
       Serializador para las armas.
       Este serializador convierte los datos de las armas (ID, nombre, daño, crítico, precisión e imagen)
       a formato JSON.
    """
    class Meta:
        model = Weapon
        fields = ['id', 'name', 'damage', 'critic', 'accuracy', 'image']  # Campos a mostrar: ID, nombre, daño, crítico, precisión e imagen

class ArmorSerializer(serializers.ModelSerializer):
    """
        Serializador para las armaduras.
        Este serializador convierte los datos de las armaduras (ID, nombre, defensa e imagen)
        a formato JSON.
    """
    class Meta:
        model = Armor
        fields = ['id', 'name', 'defense', 'image'] # Campos a mostrar: ID, nombre, defensa e imagen


class CharacterMemberSerializer(serializers.ModelSerializer):
    """
    Serializador para los miembros de una facción (personajes).
    Este serializador convierte los datos del personaje (ID y nombre) a formato JSON.
    """
    class Meta:
        model = Character
        fields = ['id', 'name']  # Campos a mostrar: ID y nombre del personaje

class FactionSerializer(serializers.ModelSerializer):
    """
    Serializador para la facción.
    Este serializador convierte los datos de la facción (ID, nombre, ubicación y miembros)
    a formato JSON. Los miembros se serializan utilizando el `CharacterMemberSerializer`.
    """
    members = CharacterMemberSerializer(many=True, read_only=True)  # Serializa los miembros de la facción

    class Meta:
        model = Faction
        fields = ['id', 'name', 'location', 'members']  # Campos a mostrar: ID, nombre, ubicación y miembros

class RelationshipSerializer(serializers.ModelSerializer):
    """
    Serializador para la relación entre dos personajes.
    Este serializador convierte los datos de una relación entre dos personajes a formato JSON.
    """
    class Meta:
        model = Relationship
        fields = ['character1_id', 'character2_id', 'relationship_type']  # Campos a mostrar: IDs de los personajes y tipo de relación

class InventorySerializer(serializers.ModelSerializer):
    """
    Serializador para el inventario de un personaje.
    Este serializador convierte los datos de las armas y armaduras del inventario a formato JSON.
    """
    weapons = WeaponSerializer(many=True, read_only=True)  # Serializa las armas del inventario
    armors = ArmorSerializer(many=True, read_only=True)  # Serializa las armaduras del inventario

    class Meta:
        model = Inventory
        fields = ['character_id','weapons', 'armors']  # Campos a mostrar: ID del personaje, armas y armaduras

class FactionCharacterCountModelSerializer(serializers.ModelSerializer):
    """
    Serializador para obtener el conteo de personajes de una facción.
    Este serializador devuelve el nombre de la facción y la cantidad de personajes que tiene.
    """
    character_count = serializers.SerializerMethodField()

    class Meta:
        model = Faction
        fields = ['name', 'character_count']  # Campos a mostrar: nombre de la facción y conteo de personajes

    def get_character_count(self, obj):
        """
        Método para obtener el número de miembros de una facción.
        Cuenta cuántos personajes están asociados a esta facción.
        """
        return obj.members.count()  # `members` es el `related_name` de `Character`

class CharacterSerializer(serializers.ModelSerializer):
    """
    Serializador para los detalles de un personaje.
    Este serializador convierte los datos del personaje (incluyendo facción, armas, armaduras,
    relaciones e inventario) a formato JSON.
    """
    faction = FactionSerializer()  # Relación anidada con el serializador de la facción
    equipped_weapon = WeaponSerializer()  # Relación anidada con el serializador del arma equipada
    equipped_armor = ArmorSerializer()  # Relación anidada con el serializador de la armadura equipada
    relationships = serializers.SerializerMethodField()  # Método para obtener las relaciones del personaje
    inventory = InventorySerializer()  # Relación anidada con el serializador del inventario

    class Meta:
        model = Character
        fields = ['id', 'name', 'location', 'image', 'faction', 'equipped_weapon', 'equipped_armor', 'relationships', 'inventory']  # Campos a mostrar del personaje

    def get_relationships(self, obj):
        """
        Método para obtener las relaciones de un personaje con otros personajes.
        Utiliza la clase `RelationshipSerializer` para serializar todas las relaciones
        en las que el personaje está involucrado.
        """
        relationships = Relationship.objects.filter(
            Q(character1=obj) | Q(character2=obj)  # Filtra las relaciones donde el personaje esté involucrado
        )
        # Serializa las relaciones y las devuelve en formato JSON
        return RelationshipSerializer(relationships, many=True).data
