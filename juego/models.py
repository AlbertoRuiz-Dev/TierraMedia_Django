from django.db import models

# Create your models here.
#Branch subida

class Weapon(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    damage = models.IntegerField(default=0)
    description = models.TextField(max_length=100)

class Armor(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    defense = models.IntegerField(default=0)
    description = models.TextField(max_length=100)

class Equipment(models.Model):
    weapon = models.ForeignKey(Weapon, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    armor = models.ForeignKey(Armor, on_delete=models.SET_NULL, null=True, blank=True, default=None)

class Character(models.Model):
    name = models.CharField(max_length=50)
    inventory = models.OneToOneField(Equipment, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    armor_equipped = models.OneToOneField(Armor, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    weapon_equipped = models.OneToOneField(Weapon, on_delete=models.SET_NULL, null=True, blank=True, default=None)