from rest_framework import serializers
from juego.models import *

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'