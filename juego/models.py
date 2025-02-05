from django.db import models

# Create your models here.
class Faction(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.location})"

class Weapon(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default="Tan vago como siempre... sin descripción")
    damage = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} (Daño: {self.damage})"

class Armor(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default="Tan vago como siempre... sin descripción")
    defense = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} (Defensa: {self.defense})"

class Character(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    faction = models.ForeignKey(Faction, on_delete=models.SET_NULL, null=True, blank=True, related_name="members")
    equipped_weapon = models.ForeignKey(Weapon, on_delete=models.SET_NULL, null=True, blank=True,related_name="equipped_weapon")
    equipped_armor = models.ForeignKey(Armor, on_delete=models.SET_NULL, null=True, blank=True, related_name="equipped_armor")

    def __str__(self):
        faction_name = self.faction.name if self.faction else "Sin Facción"
        return f"{self.name} ({faction_name}) - Ubicación: {self.location}"

class Inventory(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name="inventory")
    weapons = models.ManyToManyField(Weapon, blank=True, related_name="inventory_weapons")
    armors = models.ManyToManyField(Armor, blank=True, related_name="inventory_armors")
    def __str__(self):
        return f"Equipo de {self.character.name}"

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

    class Meta:
        unique_together = ('character1', 'character2')