from django.test import TestCase

from juego.models import *


class TestModels(TestCase):
    def setUp(self):
        self.arma = Weapon.objects.create(name="Daga", type="Arma", description="Prueba", damage=10)
        self.armadura = Armor.objects.create(name="Armadura", type="Armadura", description="Prueba", defense=10)

        self.equipamiento_arma = self.arma
        self.equipamiento_armadura = self.armadura

        self.personaje = Character.objects.create(name="Rodolfo", weapon_equipped=self.arma, armor_equipped=self.armadura)
        self.personaje.inventory.add(self.equipamiento_arma)
        self.personaje.inventory.add(self.equipamiento_armadura)


    def test_character(self):
        self.assertEqual(self.personaje.inventory.count(), 2)
        self.assertIn(self.arma.id, self.personaje.inventory.values_list('id', flat=True))
        self.assertIn(self.armadura.id, self.personaje.inventory.values_list('id', flat=True))

        self.assertIn(self.personaje, self.arma.characters_equipped_weapon.all())
        self.assertIn(self.personaje, self.armadura.characters_equipped_armor.all())

        self.assertIn(self.personaje, self.arma.characters_with_item.all())
        self.assertIn(self.personaje, self.armadura.characters_with_item.all())

        self.assertEqual(self.personaje.weapon_equipped.name, "Daga")
        self.assertEqual(self.personaje.armor_equipped.name, "Armadura")
