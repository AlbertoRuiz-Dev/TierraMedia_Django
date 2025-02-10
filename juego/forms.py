from django import forms
from juego.models import *

class FactionForm(forms.ModelForm):
    faction = forms.ModelChoiceField(
        queryset=Faction.objects.all(),
        widget=forms.Select(),
        label="Selecciona una facción:"
    )

class EquipmentForm(forms.ModelForm):
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

class WeaponForm(forms.ModelForm):
    class Meta:
        model = Weapon
        fields = ['name', 'description', 'damage','image']
