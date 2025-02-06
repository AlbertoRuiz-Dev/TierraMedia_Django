from django import forms
from juego.models import *
from itertools import chain

class FactionForm(forms.Form):
    faction = forms.ModelChoiceField(
        queryset=Faction.objects.all(),
        widget=forms.Select(),
        label="Selecciona una facción"
    )

class EquipmentForm(forms.Form):
    Equipment = forms.ModelChoiceField(
        queryset=chain(Weapon.objects.all(), Armor.objects.all()),
        widget=forms.Select(),
        label="Selecciona un arma o armadura"
    )