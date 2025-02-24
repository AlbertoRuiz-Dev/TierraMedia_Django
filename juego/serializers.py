from rest_framework import serializers
from .models import Character, Weapon, Armor

class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = ['id', 'name', 'damage', 'critic', 'accuracy', 'image']

class ArmorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Armor
        fields = ['id', 'name', 'defense', 'image']

class CharacterSerializer(serializers.ModelSerializer):
    equipped_weapon = WeaponSerializer(read_only=True)  # Incluir detalles del arma
    equipped_armor = ArmorSerializer(read_only=True)    # Incluir detalles de la armadura

    class Meta:
        model = Character
        fields = ['id', 'name', 'location', 'image', 'faction', 'equipped_weapon', 'equipped_armor']