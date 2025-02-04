from django.db import models

# Create your models here.
#Branch subida

class Weapon(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    damage = models.IntegerField(default=0)


class Armor(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    defense = models.IntegerField(default=0)


class Equipment(models.Model):
    name = models.CharField(max_length=50)
    weapon = models.OneToOneField(Weapon, on_delete=models.CASCADE, primary_key=True, blank=True)
    armor = models.OneToOneField(Armor, on_delete=models.CASCADE, primary_key=True, blank=True)
    description = models.TextField(max_length=100)


class Character(models.Model):
    name = models.CharField(max_length=50)
    inventory = [models.ManyToManyField(Equipment)]
    armor_equipped = models.ManyToManyField(Armor)
    weapon_equipped = models.ManyToManyField(Weapon)