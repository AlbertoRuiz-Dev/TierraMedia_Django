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
        fields = ['id', 'name', 'damage', 'critic', 'accuracy']  # Campos a mostrar: ID, nombre, daño, crítico, precisión e imagen

class ArmorSerializer(serializers.ModelSerializer):
    """
        Serializador para las armaduras.
        Este serializador convierte los datos de las armaduras (ID, nombre, defensa e imagen)
        a formato JSON.
    """
    class Meta:
        model = Armor
        fields = ['id', 'name', 'defense'] # Campos a mostrar: ID, nombre, daño, defensa e imagen


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

    # Se utiliza PrimaryKeyRelatedField para representar las relaciones a través de los IDs de los personajes
    character1 = serializers.PrimaryKeyRelatedField(queryset=Character.objects.all().select_related('faction'))
    character2 = serializers.PrimaryKeyRelatedField(queryset=Character.objects.all().select_related('faction'))

    class Meta:
        model = Relationship
        fields = ['character1', 'character2', 'relationship_type']  # Campos a mostrar: IDs de los personajes y tipo de relación

    def validate(self, data):
        """
        Asegura que un personaje no pueda tener una relación consigo mismo.
        """
        if data['character1'] == data['character2']:
            raise serializers.ValidationError("Un personaje no puede tener una relación consigo mismo.")
        return data

class InventorySerializer(serializers.ModelSerializer):
    """
    Serializador para el inventario de un personaje.
    Este serializador convierte los datos de las armas y armaduras del inventario a formato JSON.
    """
    # Se utiliza PrimaryKeyRelatedField para representar las relaciones a través de los IDs de las armas
    weapons = serializers.PrimaryKeyRelatedField(queryset=Weapon.objects.all(), many=True)

    # Se utiliza PrimaryKeyRelatedField para representar las relaciones a través de los IDs de las armaduras
    armors = serializers.PrimaryKeyRelatedField(queryset=Armor.objects.all(), many=True)

    # Se utiliza PrimaryKeyRelatedField para representar las relaciones a través de los IDs de los personajes
    character = serializers.PrimaryKeyRelatedField(queryset=Character.objects.all().select_related('faction'))

    class Meta:
        model = Inventory
        fields = ['character','weapons', 'armors']  # Campos a mostrar: ID del personaje, armas y armaduras



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
        return obj.members.count()  # members es el related_name de Character

class InventorySerializerDefault(serializers.ModelSerializer):
    """
    Serializador para el inventario de un personaje.
    Este serializador convierte los datos de las armas y armaduras del inventario a formato JSON.
    """

    # Serializa las armas del inventario utilizando el serializador WeaponSerializer
    weapons = WeaponSerializer(many=True)  # Permite múltiples armas para cada inventario

    # Serializa las armaduras del inventario utilizando el serializador ArmorSerializer
    armors = ArmorSerializer(many=True)  # Permite múltiples armaduras para cada inventario

    # Representa la relación entre el inventario y el personaje mediante un PrimaryKeyRelatedField
    character = serializers.PrimaryKeyRelatedField(queryset=Character.objects.all())  # Relaciona el inventario con un personaje específico

    class Meta:
        model = Inventory  # Especifica el modelo de este serializador
        fields = ['character', 'weapons', 'armors']  # Campos a mostrar: el ID del personaje, las armas y las armaduras


class CharacterSerializer(serializers.ModelSerializer):
    """
    Serializador para los detalles de un personaje.
    Este serializador convierte los datos del personaje a formato JSON.
    """

    class Meta:
        model = Character
        fields = ['id', 'name']  # Campos a mostrar del personaje


class RelationshipSerializerDefault(serializers.ModelSerializer):
    """
    Serializador para la relación entre dos personajes.
    Este serializador convierte los datos de una relación entre dos personajes a formato JSON.
    """

    # Serializa los datos de los dos personajes involucrados en la relación
    character1 = CharacterSerializer()  # Primer personaje en la relación
    character2 = CharacterSerializer()  # Segundo personaje en la relación

    class Meta:
        model = Relationship  # Especifica el modelo relacionado con este serializador
        fields = ['character1', 'character2', 'relationship_type']  # Campos a mostrar: los personajes involucrados y el tipo de relación

    def validate(self, data):
        """
        Asegura que un personaje no pueda tener una relación consigo mismo.
        Si los dos personajes son iguales, se lanza una excepción de validación.
        """
        if data['character1'] == data['character2']:  # Verifica si ambos personajes son el mismo
            raise serializers.ValidationError("Un personaje no puede tener una relación consigo mismo.")  # Lanza error si son iguales
        return data  # Retorna los datos validados si no hay errores


class CharacterSerializerAll(serializers.ModelSerializer):
    """
    Serializador para los detalles de un personaje.
    Este serializador convierte los datos del personaje (incluyendo facción, armas, armaduras,
    relaciones e inventario) a formato JSON.
    """
    # Relación anidada con el serializador de la facción
    faction = FactionSerializer()  # Esto mostrará los detalles de la facción (por nombre, etc.)

    # Relación anidada con el serializador del arma equipada
    equipped_weapon = WeaponSerializer()  # Esto mostrará los detalles del arma equipada

    # Relación anidada con el serializador de la armadura equipada
    equipped_armor = ArmorSerializer()  # Esto mostrará los detalles de la armadura equipada

    # Método para obtener las relaciones del personaje
    relationships = serializers.SerializerMethodField()

    # Relación anidada con el serializador del inventario
    inventory = InventorySerializerDefault()  # Esto mostrará los detalles del inventario

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
        ).prefetch_related('character1', 'character2')
        # Serializa las relaciones y las devuelve en formato JSON
        return RelationshipSerializerDefault(relationships, many=True).data

class CharacterSerializerModify(serializers.ModelSerializer):
    """
    Serializador para modificar/eliminar un personaje.
    Este serializador convierte los datos del personaje (incluyendo facción, armas, armaduras,
    relaciones e inventario) a formato JSON.
    """

    # Relación con la facción, acepta el ID de la facción
    faction = serializers.PrimaryKeyRelatedField(queryset=Faction.objects.all(), required=False) # Permite modificar la facción del personaje. No es obligatorio proporcionarlo.

    # Relación con el arma equipada, acepta el ID del arma equipada
    equipped_weapon = serializers.PrimaryKeyRelatedField(queryset=Weapon.objects.all(), required=False) # Permite modificar el arma equipada del personaje. No es obligatorio.

    # Relación con la armadura equipada, acepta el ID de la armadura equipada
    equipped_armor = serializers.PrimaryKeyRelatedField(queryset=Armor.objects.all(), required=False) # Permite modificar la armadura equipada del personaje. No es obligatorio.


    class Meta:
        model = Character  # Especifica que el modelo que estamos serializando es `Character`.
        fields = [
            'id', 'name', 'location', 'faction',
            'equipped_weapon', 'equipped_armor'
        ]  # Campos a mostrar del personaje, que incluyen `id`, `name`, `location`, `image`, etc.

    def get_relationships(self, obj):
        """
        Método para obtener las relaciones de un personaje con otros personajes.
        Utiliza la clase `RelationshipSerializer` para serializar todas las relaciones
        en las que el personaje está involucrado.
        """
        # Filtra las relaciones donde el personaje esté involucrado, ya sea como `character1` o `character2`
        relationships = Relationship.objects.filter(
            Q(character1=obj) | Q(character2=obj)  # Filtra las relaciones donde el personaje está involucrado
        )
        # Serializa las relaciones encontradas y las devuelve en formato JSON
        return RelationshipSerializer(relationships, many=True).data
