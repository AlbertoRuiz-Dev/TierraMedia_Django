from django import forms
from django.template.context_processors import request


from .models import *

class RelacionesForm(forms.Form):
    relation1 = forms.ModelChoiceField(
        queryset = Character.objects.all(),
        widget= forms.Select(),
        label= "Personaje1")

    relation2 = forms.ModelChoiceField(
        queryset=Character.objects.all(),
        widget=forms.Select(),
        label="Personaje2")


