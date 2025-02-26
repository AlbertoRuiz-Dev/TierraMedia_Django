from django.core.exceptions import ValidationError
from django.db import models
import random
# Create your models here.
from django.contrib.auth.models import User


class Faction(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.location})"

class Weapon(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default="Tan vago como siempre... sin descripción")
    damage = models.IntegerField(default=0)
    critic = models.IntegerField(blank=True, null=True)
    accuracy = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='weapons/', null=True, blank=True, default='weapons/default_weapon.jpg')


    def save(self, *args, **kwargs):
        if self.critic is None:  # Solo generar si no tiene valor
            self.critic = random.randint(0, 90)
        if self.accuracy is None:
            self.accuracy = random.randint(40, 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Daño: {self.damage})"

class Armor(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default="Tan vago como siempre... sin descripción")
    defense = models.IntegerField(default=0)
    image = models.ImageField(upload_to='armors/', null=True, blank=True, default='armors/default_armor.jpg')


    def __str__(self):
        return f"{self.name} (Defensa: {self.defense})"

class Character(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    faction = models.ForeignKey(Faction, on_delete=models.SET_NULL, null=True, blank=True, related_name="members")
    equipped_weapon = models.ForeignKey(Weapon, on_delete=models.SET_NULL, null=True, blank=True,related_name="equipped_weapon")
    equipped_armor = models.ForeignKey(Armor, on_delete=models.SET_NULL, null=True, blank=True, related_name="equipped_armor")
    image = models.ImageField(upload_to='characters/', null=True, blank=True, default='characters/default_character.jpg')

    def __str__(self):
        faction_name = self.faction.name if self.faction else "Sin Facción"
        return f"{self.name} ({faction_name})"

class Inventory(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name="inventory")
    weapons = models.ManyToManyField(Weapon, blank=True, related_name="inventory_weapons")
    armors = models.ManyToManyField(Armor, blank=True, related_name="inventory_armors")
    def __str__(self):
        return f"Equipo de {self.character.name}, Armas: {[weapon.name for weapon in self.weapons.all()]}, Armadura: {[armor.name for armor in self.armors.all()]}"

class Relationship(models.Model):
    character1 = models.ForeignKey(Character, related_name='relationships1', on_delete=models.CASCADE)
    character2 = models.ForeignKey(Character, related_name='relationships2', on_delete=models.CASCADE)
    relationship_type = models.CharField(max_length=50, choices=[
        ('friend', 'Amigo'),
        ('enemy', 'Enemigo'),
        ('ally', 'Aliado'),
        ('rival', 'Rival'),
        ('neutral', 'Neutral'),
    ], default='neutral')

    def __str__(self):
        return f"{self.character1.name} - {self.character2.name} ({self.get_relationship_type_display()})"

    def clean(self):
        if self.character1 == self.character2:
            raise ValidationError("No se puede realizar una relación con la misma persona")

    class Meta:
        unique_together = [['character1', 'character2']]

