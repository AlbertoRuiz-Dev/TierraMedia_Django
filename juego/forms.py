from django import forms
from .models import *

class RelationForm(forms.Form):
    relation1 = forms.ModelChoiceField(
        queryset=Character.objects.all(),
        widget= forms.Select(),
        label= "Personaje1")

    relation2 = forms.ModelChoiceField(
        queryset=Character.objects.all(),
        widget=forms.Select(),
        label="Personaje2")

class FactionForm(forms.Form):
    faction = forms.ModelChoiceField(
        queryset=Faction.objects.all(),
        widget=forms.Select(),
        label="Selecciona una facción: ")

class EquipmentForm(forms.Form):
    # Campo para seleccionar un arma
    weapon = forms.ModelChoiceField(
        queryset=Weapon.objects.all(),
        widget=forms.Select(),
        label="Selecciona un arma:",
        required=False  # Hacemos el campo opcional
    )

    # Campo para seleccionar una armadura
    armor = forms.ModelChoiceField(
        queryset=Armor.objects.all(),
        widget=forms.Select(),
        label="Selecciona una armadura:",
        required=False  # Hacemos el campo opcional
    )