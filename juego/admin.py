from django.contrib import admin
from .models import *
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

# Register your models here.

# Registro del modelo Faction en el panel de administración de Django   (En principio no se usa)
@admin.register(Faction)
class FactionModelAdmin(admin.ModelAdmin):
    # Personalización de los campos en el formulario del modelo
    formfield_overrides = {
        # Se usa el widget JSONEditorWidget para campos del tipo JSONField
        JSONField: {'widget': JSONEditorWidget},
    }

# Registro de los modelos restantes en el panel de administración de Django
admin.site.register(Weapon)  # Registro del modelo Weapon
admin.site.register(Armor)   # Registro del modelo Armor
admin.site.register(Character)  # Registro del modelo Character
admin.site.register(Inventory)  # Registro del modelo Inventory
admin.site.register(Relationship)  # Registro del modelo Relationship





