from django import forms
from juego.models import *


class FactionForm(forms.Form):
    faction = forms.ModelChoiceField(
        queryset=Faction.objects.all(),
        widget=forms.Select(),
        label="Selecciona una facción"
    )

class EquipmentForm(forms.Form):
    Equipment = forms.ModelChoiceField(
        queryset=Weapon.objects.all(),
        widget=forms.Select(),
        label="Selecciona un arma o armadura"
    )