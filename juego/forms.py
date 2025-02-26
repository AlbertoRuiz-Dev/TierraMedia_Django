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
        fields = ['name', 'location', 'faction', 'equipped_weapon', 'equipped_armor']


class FactionDefaultForm(forms.ModelForm):
    class Meta:
        model = Faction  # Vincula el formulario al modelo Faccion
        fields = ["name", "location"]  # Campos que se incluirán en el formulario

class RelationshipForm(forms.ModelForm):
    class Meta:
        model = Relationship
        fields = ['character1', 'relationship_type', 'character2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['character1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Personaje 1'})
        self.fields['relationship_type'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Tipo de Relación'})
        self.fields['character2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Personaje 2'})