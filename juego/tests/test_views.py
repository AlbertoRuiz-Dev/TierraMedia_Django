from django.contrib.auth.models import User
from django.template.context_processors import request
from django.test import TestCase
from django.urls import reverse
from juego.models import *
from django.test import Client

"""
Este módulo contiene pruebas unitarias para las vistas de autenticación y gestión de personajes

Incluye pruebas para:
- Inicio y cierre de sesión
- Listado de personajes y sus atributos
- Formulario de selección de facción
- Formulario de equipamiento de personajes
"""

class LoginViewTest(TestCase):
    """Pruebas para la vista de inicio de sesión"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login_view(self):
        """Verifica que el login funciona correctamente"""

        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)  # Status OK

class LogoutViewTest(TestCase):
    """Pruebas para la vista de cierre de sesión"""

    def setUp(self):
        """
            Configuración inicial de los datos de prueba
            Crea un usuario de prueba
        """
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_logout_view(self):
        """Verifica que el usuario se desloguea correctamente y se muestra la plantilla adecuada"""
        self.client.login(username='testuser', password='password123')

        response = self.client.post(reverse('logout'))  # Hacer logout con POST
        self.assertTemplateUsed(response, 'registration/logged_out.html')


class FactionCharacterFormViewTest(TestCase):
    """Pruebas para la vista de filtrar los personajes por una facción"""

    def setUp(self):
        """
            Configuración inicial de los datos de prueba.
            Crea facciones, personajes y un usuario de prueba
        """
        self.faction1 = Faction.objects.create(name="Aliados", location="Rohan")
        self.faction2 = Faction.objects.create(name="Prueba2_faccion", location="Prueba2_localizacion")
        self.faction3 = Faction.objects.create(name="Prueba3_faccion", location="Prueba3_localizacion")
        self.character = Character.objects.create(name="Legolas", location="Rohan", faction=self.faction1)
        self.character2 = Character.objects.create(name="Gimli", location="Montañas Nubladas", faction=None)
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.faction_character_form_url = reverse('juego:factionCharacterFormView')

    def test_redirect_if_not_logged_in(self):
        """ Verifica que un usuario no autenticado sea redirigido al login """
        response = self.client.get(self.faction_character_form_url)
        self.assertRedirects(response, f"/accounts/login/?next={self.faction_character_form_url}")

    def test_character_list_template_render(self):
        """Verifica que la plantilla se renderiza correctamente y muestra las facciones y los personajes"""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.faction_character_form_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'juego/faction_character_list.html')

        self.assertContains(response, "Legolas")  # Personaje
        self.assertContains(response, "Gimli")  # Personaje
        self.assertContains(response, "Aliados")  # Facción
        self.assertContains(response, "Prueba2_faccion")  # Facción
        self.assertContains(response, "Prueba3_faccion")  # Facción


    def test_faction_form(self):
        """Verifica que un personaje pueda ser filtrado por facción."""

        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.faction_character_form_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Legolas")  # Personaje
        self.assertContains(response, "Gimli")  # Personaje

        response = self.client.post(self.faction_character_form_url, {'faction': self.faction1.id})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Legolas")  # Personaje
        self.assertNotContains(response, "Gimli")  # Personaje

    def tearDown(self):
        """
            Limpieza de los datos de prueba.
            Elimina facciones, personajes y el usuario de prueba.
        """

        # Eliminar personajes
        Character.objects.all().delete()

        # Eliminar facciones
        Faction.objects.all().delete()

        # Eliminar usuario
        User.objects.all().delete()


class EquipmentCharacterFormViewTest(TestCase):
    """Pruebas para la vista de filtrar los personajes por un equipamiento específico"""

    def setUp(self):
        """
            Configuración inicial de los datos de prueba.
            Crea armas, armaduras, personajes y un usuario de prueba
        """
        self.weapon1 = Weapon.objects.create(name="Arco", description="Arco largo", damage=12)
        self.weapon2 = Weapon.objects.create(name="Espada corta", description="Espada afilada", damage=8)
        self.armor1 = Armor.objects.create(name="Armadura ligera", description="Armadura de cuero", defense=5)
        self.armor2 = Armor.objects.create(name="Armadura pesada", description="Armadura de placas", defense=15)
        self.character = Character.objects.create(name="Legolas", location="Rohan", faction=None, equipped_armor=self.armor1, equipped_weapon=self.weapon1)
        self.character2 = Character.objects.create(name="Gimli", location="Montañas Nubladas", faction=None)
        self.character3 = Character.objects.create(name="Prueba3", location="Prueba3", faction=None, equipped_armor=self.armor2, equipped_weapon=self.weapon2)
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.equipment_character_form_url = reverse('juego:equipmentCharacterFormView')

    def test_redirect_if_not_logged_in(self):
        """Verifica que un usuario no autenticado sea redirigido al login """
        response = self.client.get(self.equipment_character_form_url)
        self.assertRedirects(response, f"/accounts/login/?next={self.equipment_character_form_url}")

    def test_character_list_template_render(self):
        """Verifica que la plantilla se renderiza correctamente y muestra las armas, armaduras y los personajes"""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.equipment_character_form_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'juego/equipment_character_list.html')

        self.assertContains(response, "Legolas")  # Personaje
        self.assertContains(response, "Gimli")  # Personaje
        self.assertContains(response, "Arco")  # Arma
        self.assertContains(response, "Espada corta")  # Arma
        self.assertContains(response, "Armadura ligera")  # Armadura
        self.assertContains(response, "Armadura pesada")  # Armadura

    def test_equipment_form(self):
        """Verifica que un personaje sin inventario ni facción muestra 'Vacio' y 'No hay inventario'"""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.equipment_character_form_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Legolas")  # Personaje
        self.assertContains(response, "Gimli")  # Personaje
        self.assertContains(response, "Prueba3")  # Personaje

        response = self.client.post(self.equipment_character_form_url, {'weapon': self.weapon1.id, 'armor': self.armor1.id})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Legolas")  # Personaje
        self.assertNotContains(response, "Gimli")  # Personaje
        self.assertNotContains(response, "Prueba3")  # Personaje

        response = self.client.post(self.equipment_character_form_url, {'weapon': self.weapon1.id})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Legolas")  # Personaje
        self.assertNotContains(response, "Gimli")  # Personaje
        self.assertNotContains(response, "Prueba3")  # Personaje

        response = self.client.post(self.equipment_character_form_url, {'weapon': self.weapon2.id, 'armor': self.armor2.id})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Prueba3")  # Personaje
        self.assertNotContains(response, "Legolas")  # Personaje
        self.assertNotContains(response, "Gimli")  # Personaje

    def tearDown(self):
        """
            Limpieza de los datos de prueba.
            Elimina armas, armaduras, personajes y el usuario de prueba.
        """

        # Eliminar personajes
        Character.objects.all().delete()

        # Eliminar armas y armaduras
        Weapon.objects.all().delete()
        Armor.objects.all().delete()

        # Eliminar usuario
        User.objects.all().delete()

class FactionCreateViewTest(TestCase):
    """Pruebas para la vista de crear facciones"""

    def setUp(self):
        """
            Configuración inicial de los datos de prueba.
            Crea un usuario de prueba
        """
        # Eliminar facciones
        Faction.objects.all().delete()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.faction_create_url = reverse('juego:factionCreateView')


    def test_redirect_if_not_logged_in(self):
        """Verifica que un usuario no autenticado debe ser redirigido al login """
        response = self.client.get(self.faction_create_url)
        self.assertRedirects(response, f"/accounts/login/?next={self.faction_create_url}")

    def test_faction_creation(self):
        """Verifica que un usuario autenticado puede crear una facción """
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.faction_create_url, {'name': 'Hermandad', 'location': 'Bosque'})

        # Verificar redirección después de la creación
        self.assertRedirects(response, reverse('juego:factionView'))

        # Verificar que la facción se creó correctamente
        self.assertEqual(Faction.objects.count(), 1)
        faction = Faction.objects.first()
        self.assertEqual(faction.name, 'Hermandad')
        self.assertEqual(faction.location, 'Bosque')

    def tearDown(self):
        """
            Limpieza de los datos de prueba.
            Elimina facciones y el usuario de prueba.
        """

        # Eliminar facciones
        Faction.objects.all().delete()

        # Eliminar usuario
        User.objects.all().delete()

class FactionUpdateViewTest(TestCase):
    """Pruebas para la vista de actualizar facciones"""

    def setUp(self):
        """
            Configuración inicial de los datos de prueba.
            Crea un usuario y una facción de prueba
        """
        # Eliminar facciones
        Faction.objects.all().delete()
        self.faction = Faction.objects.create(name='Hermandad', location='Bosque')
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.faction_update_url = reverse('juego:factionUpdateView', args={self.faction.id})

    def test_redirect_if_not_logged_in(self):
        """Verifica que un usuario no autenticado debe ser redirigido al login """
        response = self.client.get(self.faction_update_url)
        self.assertRedirects(response, f"/accounts/login/?next={self.faction_update_url}")

    def test_faction_update(self):
        """Verifica que un usuario autenticado puede actualizar una facción """
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.faction_update_url, {'name': 'Actualizado', 'location': 'Actualizado'})

        # Verificar redirección después de la modificación
        self.assertRedirects(response, reverse('juego:factionView'))

        # Verificar que la facción se modificó correctamente
        self.assertEqual(Faction.objects.count(), 1)
        faction = Faction.objects.first()
        self.assertEqual(faction.name, 'Actualizado')
        self.assertEqual(faction.location, 'Actualizado')

    def tearDown(self):
        """
            Limpieza de los datos de prueba.
            Elimina facciones y el usuario de prueba.
        """

        # Eliminar facciones
        Faction.objects.all().delete()

        # Eliminar usuario
        User.objects.all().delete()

class FactionDetailViewTest(TestCase):
    """Pruebas para la vista de detalles de faccion"""

    def setUp(self):
        """
            Configuración inicial de los datos de prueba.
            Crea un usuario, un personaje y una facción de prueba
        """
        # Eliminar personajes
        Character.objects.all().delete()
        # Eliminar facciones
        Faction.objects.all().delete()
        self.faction = Faction.objects.create(name='Hermandad', location='Bosque')
        self.character = Character.objects.create(name="Legolas", location="Rohan", faction=self.faction,)
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.faction_detail_url = reverse('juego:factionDetailView', args={self.faction.id})

    def test_redirect_if_not_logged_in(self):
        """Verifica que un usuario no autenticado debe ser redirigido al login """
        response = self.client.get(self.faction_detail_url)
        self.assertRedirects(response, f"/accounts/login/?next={self.faction_detail_url}")

    def test_faction_details(self):
        """Verifica que un usuario autenticado puede ver los detalles una facción """
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.faction_detail_url)

        # Verificar que la facción se modificó correctamente
        self.assertEqual(Faction.objects.count(), 1)
        self.assertContains(response, "Legolas")  # Personaje
        self.assertContains(response, 1)  # Personaje

    def tearDown(self):
        """
            Limpieza de los datos de prueba.
            Elimina facciones, personajes y el usuario de prueba.
        """

        # Eliminar facciones
        Faction.objects.all().delete()

        # Eliminar personajes
        Character.objects.all().delete()

        # Eliminar usuario
        User.objects.all().delete()

class FactionDeleteViewTest(TestCase):
    """Pruebas para la vista de eliminar facciones"""

    def setUp(self):
        """
            Configuración inicial de los datos de prueba.
            Crea una facción y un usuario de prueba
        """
        # Eliminar facciones
        Faction.objects.all().delete()
        self.faction = Faction.objects.create(name='Hermandad', location='Bosque')
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.faction_create_url = reverse('juego:factionDeleteView', args={self.faction.id})


    def test_redirect_if_not_logged_in(self):
        """Verifica que un usuario no autenticado debe ser redirigido al login"""
        response = self.client.get(self.faction_create_url)
        self.assertRedirects(response, f"/accounts/login/?next={self.faction_create_url}")

    def test_faction_delete(self):
        """Verifica que un usuario autenticado puede eliminar una facción"""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.faction_create_url, {'pk': 1})

        # Verificar redirección después de la eliminación
        self.assertRedirects(response, reverse('juego:factionView'))

        # Verificar que la facción se eliminó correctamente
        self.assertEqual(Faction.objects.count(), 0)

    def tearDown(self):
        """
            Limpieza de los datos de prueba.
            Elimina facciones y el usuario de prueba.
        """

        # Eliminar facciones
        Faction.objects.all().delete()

        # Eliminar usuario
        User.objects.all().delete()
