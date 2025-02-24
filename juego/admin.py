from django.contrib import admin
from .models import *
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

# Register your models here.

@admin.register(Faction)
class FactionModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }

admin.site.register(Weapon)
admin.site.register(Armor)
admin.site.register(Character)
admin.site.register(Inventory)
admin.site.register(Relationship)




