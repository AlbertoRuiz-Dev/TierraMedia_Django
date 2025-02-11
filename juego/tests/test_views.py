from django.contrib.auth.models import User
from django.template.context_processors import request
from django.test import TestCase
from django.urls import reverse
from juego.models import *
from django.test import Client

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_view(self):
        # Verifica que el login funciona correctamente
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 200)  # Status OK

class LogoutViewTest(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_logout_view(self):
        """Verifica que el usuario se desloguea correctamente y renderiza una plantilla confirmando el deslogueo"""
        self.client.login(username='testuser', password='password123')

        response = self.client.post(reverse('logout'))  # Hacer logout con POST
        self.assertTemplateUsed(response, 'registration/logged_out.html')


class CharacterListViewTest(TestCase):
    def setUp(self):
        self.faction1 = Faction.objects.create(name="Aliados", location="Rohan")
        self.faction2 = Faction.objects.create(name="Prueba2_faccion", location="Prueba2_localizacion")
        self.faction3 = Faction.objects.create(name="Prueba3_faccion", location="Prueba3_localizacion")

        self.weapon1 = Weapon.objects.create(name="Arco", description="Arco largo", damage=12)
        self.weapon2 = Weapon.objects.create(name="Espada corta", description="Espada afilada", damage=8)
        self.armor1 = Armor.objects.create(name="Armadura ligera", description="Armadura de cuero", defense=5)
        self.armor2 = Armor.objects.create(name="Armadura pesada", description="Armadura de placas", defense=15)
        self.character = Character.objects.create(name="Legolas", location="Rohan", faction=self.faction1, equipped_armor=self.armor1, equipped_weapon=self.weapon1)
        self.inventory = Inventory.objects.create(character=self.character)
        self.inventory.weapons.add(self.weapon1, self.weapon2)
        self.inventory.armors.add(self.armor1, self.armor2)
        self.character2 = Character.objects.create(name="Gimli", location="Montañas Nubladas", faction=None)
        Relationship.objects.create(character1=self.character, character2=self.character2, relationship_type="friend")
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.character_list_url = reverse('juego:characterListView')

    def test_redirect_if_not_logged_in(self):
        """ Un usuario no autenticado debe ser redirigido al login """
        response = self.client.get(self.character_list_url)
        self.assertRedirects(response, f"/accounts/login/?next={self.character_list_url}")

    def test_character_list_template_render(self):
        """Verifica que la plantilla se renderiza correctamente y muestra los datos del personaje"""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.character_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'juego/character_list.html')

        # Verificar que el personaje "Legolas" aparece en el HTML
        self.assertContains(response, "Legolas")
        self.assertContains(response, "Rohan")  # Ubicación del personaje
        self.assertContains(response, "Aliados")  # Facción


    def test_character_list_shows_inventory(self):
        """Verifica que se muestra el inventario del personaje"""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.character_list_url)

        self.assertContains(response, "Espada corta (Daño: 8)")  # Arma en inventario
        self.assertContains(response, "Arco (Daño: 12)")  # Arma en inventario
        self.assertContains(response, "Armadura ligera (Defensa: 5)")  # Armadura en inventario
        self.assertContains(response, "Armadura pesada (Defensa: 15)")  # Armadura en inventario

    def test_character_list_shows_equipped_items(self):
        """Verifica que se muestran los objetos equipados"""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.character_list_url)

        self.assertContains(response, "Espada corta (Daño: 8)")
        self.assertContains(response, "Armadura ligera (Defensa: 5)")

    def test_character_list_shows_relationships(self):
        """Verifica que se muestran las relaciones del personaje"""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.character_list_url)

        self.assertContains(response, "Legolas - Gimli (Amigo)")  # Relación esperada

    def test_character_without_inventory_or_faction(self):
        """Verifica que un personaje sin inventario ni facción muestra 'Vacio' y 'No hay inventario'"""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.character_list_url)

        self.assertContains(response, "Gimli")  # Otro personaje sin facción ni inventario
        self.assertContains(response, "Vacio")  # No tiene facción
        self.assertContains(response, "No hay inventario")  # No tiene armas ni armaduras

class FactionCharacterFormViewTest(TestCase):
    def setUp(self):
        self.faction1 = Faction.objects.create(name="Aliados", location="Rohan")
        self.faction2 = Faction.objects.create(name="Prueba2_faccion", location="Prueba2_localizacion")
        self.faction3 = Faction.objects.create(name="Prueba3_faccion", location="Prueba3_localizacion")
        self.character = Character.objects.create(name="Legolas", location="Rohan", faction=self.faction1)
        self.character2 = Character.objects.create(name="Gimli", location="Montañas Nubladas", faction=None)
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.faction_character_form_url = reverse('juego:factionCharacterFormView')

    def test_redirect_if_not_logged_in(self):
        """ Un usuario no autenticado debe ser redirigido al login """
        response = self.client.get(self.faction_character_form_url)
        self.assertRedirects(response, f"/accounts/login/?next={self.faction_character_form_url}")

    def test_character_list_template_render(self):
        """Verifica que la plantilla se renderiza correctamente y muestra las facciones y los personajes"""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.faction_character_form_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'juego/faction_character_list.html')

        # Verificar que el personaje "Legolas" aparece en el HTML
        self.assertContains(response, "Legolas")  # Personaje
        self.assertContains(response, "Gimli")  # Personaje
        self.assertContains(response, "Aliados")  # Facción
        self.assertContains(response, "Prueba2_faccion")  # Facción
        self.assertContains(response, "Prueba3_faccion")  # Facción


    def test_faction_form(self):
        """Verifica que un personaje sin inventario ni facción muestra 'Vacio' y 'No hay inventario'"""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.faction_character_form_url {})

        self.assertContains(response, "Gimli")  # Otro personaje sin facción ni inventario
        self.assertContains(response, "Vacio")  # No tiene facción
        self.assertContains(response, "No hay inventario")  # No tiene armas ni armaduras


