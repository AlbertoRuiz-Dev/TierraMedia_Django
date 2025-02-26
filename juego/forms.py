from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ClearableFileInput

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

class NoClearableFileInput(ClearableFileInput):
    """ Widget personalizado sin la opción de 'Clear' """
    template_name = 'widgets/no_clearable_file_input.html'  # Template para renderizar

class WeaponForm(forms.ModelForm):
    class Meta:
        model = Weapon
        fields = ['name', 'description', 'damage','image']
        widgets = {
            'image': NoClearableFileInput(),  # Asignamos el widget sin opción de limpiar
        }

class ArmorForm(forms.ModelForm):
    class Meta:
        model = Armor
        fields = ['name', 'description', 'defense', 'image']
        widgets = {
            'image': NoClearableFileInput(),  # Asignamos el widget sin opción de limpiar
        }
class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'location', 'faction', 'equipped_weapon', 'equipped_armor','image']
        widgets = {
            'image': NoClearableFileInput(),  # Asignamos el widget sin opción de limpiar
        }
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

class InventoryAddItemsForm(forms.Form):
    weapons = forms.ModelMultipleChoiceField(
        queryset=Weapon.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Armas"
    )
    # noinspection PyTypeChecker
    armors = forms.ModelMultipleChoiceField(
        queryset=Armor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Armaduras"
    )

    def __init__(self, *args, character=None, **kwargs):
        super().__init__(*args, **kwargs)
        if character and hasattr(character, 'inventory'):
            self.fields['weapons'].initial = character.inventory.weapons.all()
            self.fields['armors'].initial = character.inventory.armors.all()


class EquipWeaponForm(forms.Form):
    weapon = forms.ModelChoiceField(
        queryset=Weapon.objects.none(),
        required=False,
        label="Selecciona un arma para equipar"
    )

    def __init__(self, *args, **kwargs):
        inventory_weapons = kwargs.pop('inventory_weapons', [])
        super().__init__(*args, **kwargs)
        self.fields['weapon'].queryset = inventory_weapons
        self.fields['weapon'].empty_label = "Ninguna"

class EquipArmorForm(forms.Form):
    armor = forms.ModelChoiceField(
        queryset=Armor.objects.none(),
        required=False,
        label="Selecciona una armadura para equipar"
    )

    def __init__(self, *args, **kwargs):
        inventory_armors = kwargs.pop('inventory_armors', [])
        super().__init__(*args, **kwargs)
        self.fields['armor'].queryset = inventory_armors
        self.fields['armor'].empty_label = "Ninguna"

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    error_messages = {
        "password_mismatch": ("Las contraseñas no coinciden máquina, ESPABILA"),
    }
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user