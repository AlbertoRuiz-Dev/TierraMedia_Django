from rest_framework import serializers
from .models import *

class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = ['id', 'name', 'damage', 'critic', 'accuracy', 'image']

class ArmorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Armor
        fields = ['id', 'name', 'defense', 'image']


class CharacterMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['id', 'name']  # Agrega los campos que deseas mostrar

class FactionSerializer(serializers.ModelSerializer):
    # Usamos el CharacterSerializer para anidar los miembros de la facción
    members = CharacterMemberSerializer(many=True, read_only=True)  # Esto serializa los miembros de la facción

    class Meta:
        model = Faction
        fields = ['id', 'name', 'location', 'members']  # Añadimos 'members' a los campos

class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ['character1', 'character2', 'relationship_type']

class InventorySerializer(serializers.ModelSerializer):
    # Usamos los serializers anidados para las armas y armaduras
    weapons = WeaponSerializer(many=True, read_only=True)
    armors = ArmorSerializer(many=True, read_only=True)

    class Meta:
        model = Inventory
        fields = ['character','weapons', 'armors']

class FactionCharacterCountModelSerializer(serializers.ModelSerializer):
    character_count = serializers.SerializerMethodField()

    class Meta:
        model = Faction
        fields = ['name', 'character_count']

    def get_character_count(self, obj):
        # Contamos cuántos personajes tiene la facción
        return obj.members.count()  # `members` es el `related_name` de `Character`


class CharacterSerializer(serializers.ModelSerializer):
    # Relación anidada con Faction, Weapon, Armor, Relationship e Inventory
    faction = FactionSerializer()
    equipped_weapon = WeaponSerializer()
    equipped_armor = ArmorSerializer()
    # Esta será una propiedad que obtenemos a través de la relación de los personajes en el modelo Relationship
    relationships = serializers.SerializerMethodField()

    inventory = InventorySerializer()

    class Meta:
        model = Character
        fields = ['id', 'name', 'location', 'image', 'faction', 'equipped_weapon', 'equipped_armor', 'relationships', 'inventory']

    def get_relationships(self, obj):
        # Obtener las relaciones del personaje (Character)
        relationships_1 = Relationship.objects.filter(character1=obj)
        relationships_2 = Relationship.objects.filter(character2=obj)

        # Combinar ambas listas de relaciones y serializarlas
        all_relationships = relationships_1 | relationships_2  # Usamos el operador OR para combinar

        # Serializamos las relaciones
        return RelationshipSerializer(all_relationships, many=True).data