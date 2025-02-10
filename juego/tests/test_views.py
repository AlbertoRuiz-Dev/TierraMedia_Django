from django.contrib.auth.models import User
from django.template.context_processors import request
from django.test import TestCase
from django.urls import reverse
from juego.models import *
from django.test import Client

class ViewTests(TestCase):
    def setUp(self):
        self.faction = Faction.objects.create(name="Aliados", location="Rohan")
        self.weapon1 = Weapon.objects.create(name="Arco", description="Arco largo", damage=12)
        self.weapon2 = Weapon.objects.create(name="Espada corta", description="Espada afilada", damage=8)
        self.armor1 = Armor.objects.create(name="Armadura ligera", description="Armadura de cuero", defense=5)
        self.armor2 = Armor.objects.create(name="Armadura pesada", description="Armadura de placas", defense=15)
        self.character = Character.objects.create(name="Legolas", location="Rohan", faction=self.faction)
        self.inventory = Inventory.objects.create(character=self.character)
        self.inventory.weapons.add(self.weapon1, self.weapon2)
        self.inventory.armors.add(self.armor1, self.armor2)

    def test_login_view(self):
        # Verifica que el login funciona correctamente
        response = self.client.post(reverse('login'), {
            'username': 'admin',
            'password': 'admin',
        })
        self.assertEqual(response.status_code, 200)  # Status OK
        self.assertTemplateUsed(response, "registration/login.html")  # Comprueba contenido
