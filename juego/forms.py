from django import forms
from juego.models import *

class FactionForm(forms.Form):
    faction = forms.ModelChoiceField(
        queryset=Faction.objects.all(),
        widget=forms.Select(),
        label="Selecciona una facción:"
    )

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

class WeaponForm(forms.ModelForm):
    class Meta:
        model = Weapon
        fields = ['name', 'description', 'damage','image']

class ArmorForm(forms.ModelForm):
    class Meta:
        model = Armor
        fields = ['name', 'description', 'defense', 'image']

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'location', 'faction', 'equipped_weapon', 'equipped_armor','image']

class WeaponAddForm(forms.Form):
    weapon_id = forms.ModelChoiceField(
        queryset=Weapon.objects.all(),
        empty_label="Selecciona un arma",
        required=True,
        label="Arma"
    )

class ArmorAddForm(forms.Form):
    armor_id = forms.ModelChoiceField(
        queryset=Armor.objects.all(),
        empty_label="Selecciona una armadura",
        required=True,
        label="Armadura"
    )

class CharacterBattleForm(forms.Form):
    character = forms.ModelChoiceField(
        queryset=Character.objects.select_related('faction', 'equipped_weapon', 'equipped_armor').all(),
        widget=forms.Select(),
        label="Selecciona un personaje:"
    )

    character2 = forms.ModelChoiceField(
        queryset=Character.objects.select_related('faction', 'equipped_weapon', 'equipped_armor').all(),
        widget=forms.Select(),
        label="Selecciona otro personaje:"
    )


class FactionDefaultForm(forms.ModelForm):
    class Meta:
        model = Faction  # Vincula el formulario al modelo Faccion
        fields = ["name", "location"]  # Campos que se incluirán en el formulario