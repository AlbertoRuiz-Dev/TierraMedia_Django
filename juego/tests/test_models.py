from django.test import TestCase

from juego.models import *


class TestModels(TestCase):
    def setUp(self):
        self.arma = Weapon.objects.create(name="Daga", type="Arma", description="Prueba", damage=10)
        self.armadura = Armor.objects.create(name="Armadura", type="Armadura", description="Prueba", defense=10)

        self.equipamiento_arma = self.arma
        self.equipamiento_armadura = self.armadura

        self.personaje = Character.objects.create(name="Rodolfo")
        self.personaje.weapon_equipped.add(self.arma)
        self.personaje.armor_equipped.add(self.armadura)
        self.personaje.inventory.append(self.equipamiento_arma)
        self.personaje.inventory.append(self.equipamiento_armadura)
        self.personaje.save()

    def test_character(self):
        self.assertEqual(self.personaje.weapon_equipped.name, "Daga")