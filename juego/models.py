from django.db import models

# Create your models here.
#Branch subida

class Equipment(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    type = models.CharField(max_length=50)

class Weapon(Equipment):
    damage = models.IntegerField(default=0)

class Armor(Equipment):
    defense = models.IntegerField(default=0)

class Character(models.Model):
    name = models.CharField(max_length=50)
    inventory = models.ManyToManyField(Equipment, blank=True, related_name="characters_with_item")
    armor_equipped = models.ForeignKey(Armor, on_delete=models.SET_NULL, null=True, blank=True, related_name="characters_equipped_armor")
    weapon_equipped = models.ForeignKey(Weapon, on_delete=models.SET_NULL, null=True, blank=True, related_name="characters_equipped_weapon")
