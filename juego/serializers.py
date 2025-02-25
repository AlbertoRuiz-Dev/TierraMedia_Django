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

class FactionCharacterCountModelSerializer(serializers.ModelSerializer):
    character_count = serializers.SerializerMethodField()

    class Meta:
        model = Faction
        fields = ['name', 'character_count']

    def get_character_count(self, obj):
        # Contamos cuántos personajes tiene la facción
        return obj.members.count()  # `members` es el `related_name` de `Character`

class CharacterSerializer(serializers.ModelSerializer):
    equipped_weapon = WeaponSerializer(read_only=True)  # Incluir detalles del arma
    equipped_armor = ArmorSerializer(read_only=True)    # Incluir detalles de la armadura

    class Meta:
        model = Character
        fields = ['id', 'name', 'location', 'image', 'faction', 'equipped_weapon', 'equipped_armor']