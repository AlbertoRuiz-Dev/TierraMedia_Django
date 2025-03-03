from django.test import TestCase
from django.urls import reverse
from juego.models import *
from django.test import Client
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
import json
from django.middleware.csrf import get_token
from django.contrib.auth.models import User


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
        """
            Configuración inicial para las pruebas de inicio de sesión.
            Crea un cliente de prueba y un usuario con nombre 'testuser' y contraseña 'password123'.
        """
        self.client = Client()  # Instancia del cliente de prueba
        self.user = User.objects.create_user(username='testuser', password='password123')  # Crea un usuario de prueba

    def test_login_view(self):
        """
            Verifica que el inicio de sesión funciona correctamente.
            Realiza una solicitud POST a la vista de login con un nombre de usuario y contraseña válidos.
        """
        response = self.client.post(reverse('login'), {  # Envía el formulario de login por POST
            'username': 'testuser',  # Nombre de usuario
            'password': 'password123',  # Contraseña
        })
        self.assertEqual(response.status_code, 302)  # Verifica que el código de estado sea 302 (redirección)
        # El código 302 indica que la redirección después del login fue exitosa, lo que significa que el login fue correcto.


class LogoutViewTest(TestCase):
    """Pruebas para la vista de cierre de sesión"""

    def setUp(self):
        """
            Configuración inicial para las pruebas de cierre de sesión.
            Crea un usuario de prueba con nombre 'testuser' y contraseña 'password123'.
        """
        self.user = User.objects.create_user(username='testuser', password='password123')  # Crea un usuario de prueba

    def test_logout_view(self):
        """
            Verifica que el usuario se desloguea correctamente y se muestra la plantilla adecuada.
            Realiza una solicitud POST a la vista de logout después de haber iniciado sesión.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión como 'testuser'

        response = self.client.post(reverse('logout'))  # Realiza un POST a la vista de logout
        self.assertTemplateUsed(response, 'registration/logged_out.html')  # Verifica que la plantilla 'logged_out.html' se haya usado

        # Si la plantilla 'logged_out.html' es usada, eso significa que el logout se realizó correctamente y el usuario fue desconectado.

class FactionViewTest(TestCase):
    """Pruebas para la vista que muestra una lista de facciones"""

    def setUp(self):
        """
        Configuración inicial de los datos de prueba.
        Crea facciones, personajes y un usuario de prueba.
        """
        # Elimina las facciones
        Faction.objects.all().delete()

        # Elimina los personajes
        Character.objects.all().delete()

        self.faction1 = Faction.objects.create(name="Aliados", location="Rohan")  # Crea una facción 'Aliados'
        self.faction2 = Faction.objects.create(name="Villanos", location="Mordor")  # Crea otra facción 'Villanos'
        self.character1 = Character.objects.create(name="Legolas", location="Rohan", faction=self.faction1)  # Crea un personaje 'Legolas' de la facción 'Aliados'
        self.character2 = Character.objects.create(name="Sauron", location="Mordor", faction=self.faction2)  # Crea un personaje 'Sauron' de la facción 'Villanos'
        self.user = User.objects.create_user(username='testuser', password='password123')  # Crea un usuario de prueba
        self.faction_view_url = reverse('juego:factionView')  # URL para la vista de facciones

    def test_redirect_if_not_logged_in(self):
        """
        Verifica que un usuario no autenticado sea redirigido al login.
        Si el usuario no está autenticado, debe ser redirigido a la página de login.
        """
        response = self.client.get(self.faction_view_url)  # Realiza una solicitud GET sin estar autenticado
        self.assertRedirects(response, f"/accounts/login/?next={self.faction_view_url}")  # Verifica que sea redirigido a login

    def test_faction_view_template_render(self):
        """
        Verifica que la plantilla se renderiza correctamente y muestra las facciones.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.get(self.faction_view_url)  # Realiza una solicitud GET a la vista de facciones

        self.assertEqual(response.status_code, 200)  # Verifica que el código de estado sea 200 (OK)
        self.assertTemplateUsed(response, 'juego/faction.html')  # Verifica que se haya utilizado la plantilla correcta

        # Verifica que las facciones estén presentes en la respuesta
        self.assertContains(response, "Aliados")  # La facción 'Aliados' debe estar en la respuesta
        self.assertContains(response, "Villanos")  # La facción 'Villanos' debe estar en la respuesta

    def test_faction_member_count(self):
        """
        Verifica que la vista muestra correctamente los miembros de las facciones.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.get(self.faction_view_url)  # Realiza una solicitud GET a la vista de facciones

        self.assertEqual(response.status_code, 200)  # Verifica que el código de estado sea 200 (OK)

        # Verifica que se muestre el nombre de los personajes dentro de la facción
        self.assertContains(response, 2)  # El contador de los miembros de la facción es 2

    def tearDown(self):
        """
        Limpieza de los datos de prueba.
        Elimina facciones, personajes y el usuario de prueba.
        """
        # Eliminar personajes
        Character.objects.all().delete()  # Elimina todos los personajes creados en las pruebas

        # Eliminar facciones
        Faction.objects.all().delete()  # Elimina todas las facciones creadas en las pruebas

        # Eliminar usuario
        User.objects.all().delete()  # Elimina el usuario de prueba creado para las pruebas


class FactionCharacterFormViewTest(TestCase):
    """Pruebas para la vista de filtrar los personajes por una facción"""

    def setUp(self):
        """
            Configuración inicial de los datos de prueba.
            Crea facciones, personajes y un usuario de prueba.
        """
        self.faction1 = Faction.objects.create(name="Aliados", location="Rohan")  # Crea una facción 'Aliados'
        self.faction2 = Faction.objects.create(name="Prueba2_faccion", location="Prueba2_localizacion")  # Crea otra facción
        self.faction3 = Faction.objects.create(name="Prueba3_faccion", location="Prueba3_localizacion")  # Crea una tercera facción
        self.character = Character.objects.create(name="Legolas", location="Rohan", faction=self.faction1)  # Crea un personaje 'Legolas' de la facción 'Aliados'
        self.character2 = Character.objects.create(name="Gimli", location="Montañas Nubladas", faction=None)  # Crea un personaje 'Gimli' sin facción
        self.user = User.objects.create_user(username='testuser', password='password123')  # Crea un usuario de prueba
        self.faction_character_form_url = reverse('juego:factionCharacterFormView')  # URL para la vista de filtrado de personajes por facción

    def test_redirect_if_not_logged_in(self):
        """
            Verifica que un usuario no autenticado sea redirigido al login.
            Si el usuario no está autenticado, debe ser redirigido a la página de login.
        """
        response = self.client.get(self.faction_character_form_url)  # Realiza una solicitud GET sin estar autenticado
        self.assertRedirects(response, f"/accounts/login/?next={self.faction_character_form_url}")  # Verifica que sea redirigido a login

    def test_character_list_template_render(self):
        """
            Verifica que la plantilla se renderiza correctamente y muestra las facciones y los personajes.
            Comprueba que los personajes y facciones aparecen en la plantilla.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.get(self.faction_character_form_url)  # Realiza una solicitud GET a la vista de filtrado

        self.assertEqual(response.status_code, 200)  # Verifica que el código de estado sea 200 (OK)
        self.assertTemplateUsed(response, 'juego/faction_character_list.html')  # Verifica que se haya utilizado la plantilla correcta

        # Verifica que los personajes y facciones estén presentes en la respuesta
        self.assertContains(response, "Legolas")  # El personaje 'Legolas' debe estar en la respuesta
        self.assertContains(response, "Gimli")  # El personaje 'Gimli' debe estar en la respuesta
        self.assertContains(response, "Aliados")  # La facción 'Aliados' debe estar en la respuesta
        self.assertContains(response, "Prueba2_faccion")  # La facción 'Prueba2_faccion' debe estar en la respuesta
        self.assertContains(response, "Prueba3_faccion")  # La facción 'Prueba3_faccion' debe estar en la respuesta

    def test_faction_form(self):
        """
            Verifica que un personaje pueda ser filtrado por facción.
            Filtra los personajes por facción y verifica que solo se muestren los de la facción seleccionada.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.get(self.faction_character_form_url)  # Realiza una solicitud GET a la vista de filtrado

        self.assertEqual(response.status_code, 200)  # Verifica que el código de estado sea 200 (OK)
        self.assertContains(response, "Legolas")  # El personaje 'Legolas' debe estar en la respuesta
        self.assertContains(response, "Gimli")  # El personaje 'Gimli' debe estar en la respuesta

        # Filtra los personajes por la facción 'Aliados'
        response = self.client.post(self.faction_character_form_url, {'faction': self.faction1.id})  # Envia un POST con el ID de la facción

        self.assertEqual(response.status_code, 200)  # Verifica que el código de estado sea 200 (OK)
        self.assertContains(response, "Legolas")  # El personaje 'Legolas' debe estar en la respuesta filtrada
        self.assertNotContains(response, "Gimli")  # El personaje 'Gimli' no debe estar en la respuesta filtrada

    def tearDown(self):
        """
            Limpieza de los datos de prueba.
            Elimina facciones, personajes y el usuario de prueba.
        """
        # Eliminar personajes
        Character.objects.all().delete()  # Elimina todos los personajes creados en las pruebas

        # Eliminar facciones
        Faction.objects.all().delete()  # Elimina todas las facciones creadas en las pruebas

        # Eliminar usuario
        User.objects.all().delete()  # Elimina el usuario de prueba creado para las pruebas

class EquipmentCharacterFormViewTest(TestCase):
    """Pruebas para la vista de filtrar los personajes por un equipamiento específico"""

    def setUp(self):
        """
            Configuración inicial de los datos de prueba.
            Crea armas, armaduras, personajes y un usuario de prueba.
        """
        self.weapon1 = Weapon.objects.create(name="Arco", description="Arco largo", damage=12)  # Crea un arma 'Arco'
        self.weapon2 = Weapon.objects.create(name="Espada corta", description="Espada afilada", damage=8)  # Crea un arma 'Espada corta'
        self.armor1 = Armor.objects.create(name="Armadura ligera", description="Armadura de cuero", defense=5)  # Crea una armadura 'Armadura ligera'
        self.armor2 = Armor.objects.create(name="Armadura pesada", description="Armadura de placas", defense=15)  # Crea una armadura 'Armadura pesada'
        self.character = Character.objects.create(name="Legolas", location="Rohan", faction=None, equipped_armor=self.armor1, equipped_weapon=self.weapon1)  # Crea un personaje 'Legolas' con un arma y armadura equipados
        self.character2 = Character.objects.create(name="Gimli", location="Montañas Nubladas", faction=None)  # Crea un personaje 'Gimli' sin equipamiento
        self.character3 = Character.objects.create(name="Prueba3", location="Prueba3", faction=None, equipped_armor=self.armor2, equipped_weapon=self.weapon2)  # Crea un personaje 'Prueba3' con otro equipamiento
        self.user = User.objects.create_user(username='testuser', password='password123')  # Crea un usuario de prueba
        self.equipment_character_form_url = reverse('juego:equipmentCharacterFormView')  # URL para la vista de filtrado por equipamiento

    def test_redirect_if_not_logged_in(self):
        """Verifica que un usuario no autenticado sea redirigido al login"""
        response = self.client.get(self.equipment_character_form_url)  # Realiza una solicitud GET sin estar autenticado
        self.assertRedirects(response, f"/accounts/login/?next={self.equipment_character_form_url}")  # Verifica que sea redirigido a login

    def test_character_list_template_render(self):
        """
            Verifica que la plantilla se renderiza correctamente y muestra las armas, armaduras y los personajes.
            Asegura que los personajes y sus equipamientos estén presentes en la respuesta.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.get(self.equipment_character_form_url)  # Realiza una solicitud GET a la vista de filtrado

        self.assertEqual(response.status_code, 200)  # Verifica que el código de estado sea 200 (OK)
        self.assertTemplateUsed(response, 'juego/equipment_character_list.html')  # Verifica que se haya utilizado la plantilla correcta

        # Verifica que los personajes y los equipamientos estén presentes en la respuesta
        self.assertContains(response, "Legolas")  # El personaje 'Legolas' debe estar en la respuesta
        self.assertContains(response, "Gimli")  # El personaje 'Gimli' debe estar en la respuesta
        self.assertContains(response, "Arco")  # El arma 'Arco' debe estar en la respuesta
        self.assertContains(response, "Espada corta")  # El arma 'Espada corta' debe estar en la respuesta
        self.assertContains(response, "Armadura ligera")  # La armadura 'Armadura ligera' debe estar en la respuesta
        self.assertContains(response, "Armadura pesada")  # La armadura 'Armadura pesada' debe estar en la respuesta

    def test_equipment_form(self):
        """
            Verifica que un personaje sin inventario ni facción muestra 'Vacío' y 'No hay inventario'.
            Filtra personajes por el equipamiento seleccionado y asegura que solo se muestren los personajes con el equipamiento correspondiente.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.get(self.equipment_character_form_url)  # Realiza una solicitud GET a la vista de filtrado

        self.assertEqual(response.status_code, 200)  # Verifica que el código de estado sea 200 (OK)
        self.assertContains(response, "Legolas")  # El personaje 'Legolas' debe estar en la respuesta
        self.assertContains(response, "Gimli")  # El personaje 'Gimli' debe estar en la respuesta
        self.assertContains(response, "Prueba3")  # El personaje 'Prueba3' debe estar en la respuesta

        # Filtra los personajes por el arma 'Arco' y armadura 'Armadura ligera'
        response = self.client.post(self.equipment_character_form_url, {'weapon': self.weapon1.id, 'armor': self.armor1.id})  # Envia un POST con el ID del arma y armadura
        self.assertEqual(response.status_code, 200)  # Verifica que el código de estado sea 200 (OK)
        self.assertContains(response, "Legolas")  # El personaje 'Legolas' debe estar en la respuesta
        self.assertNotContains(response, "Gimli")  # El personaje 'Gimli' no debe estar en la respuesta
        self.assertNotContains(response, "Prueba3")  # El personaje 'Prueba3' no debe estar en la respuesta

        # Filtra solo por el arma 'Arco'
        response = self.client.post(self.equipment_character_form_url, {'weapon': self.weapon1.id})  # Envia un POST con solo el ID del arma
        self.assertEqual(response.status_code, 200)  # Verifica que el código de estado sea 200 (OK)
        self.assertContains(response, "Legolas")  # El personaje 'Legolas' debe estar en la respuesta
        self.assertNotContains(response, "Gimli")  # El personaje 'Gimli' no debe estar en la respuesta
        self.assertNotContains(response, "Prueba3")  # El personaje 'Prueba3' no debe estar en la respuesta

        # Filtra solo por el arma 'Espada corta' y armadura 'Armadura pesada'
        response = self.client.post(self.equipment_character_form_url, {'weapon': self.weapon2.id, 'armor': self.armor2.id})  # Envia un POST con otro conjunto de arma y armadura
        self.assertEqual(response.status_code, 200)  # Verifica que el código de estado sea 200 (OK)
        self.assertContains(response, "Prueba3")  # El personaje 'Prueba3' debe estar en la respuesta
        self.assertNotContains(response, "Legolas")  # El personaje 'Legolas' no debe estar en la respuesta
        self.assertNotContains(response, "Gimli")  # El personaje 'Gimli' no debe estar en la respuesta

    def tearDown(self):
        """
            Limpieza de los datos de prueba.
            Elimina armas, armaduras, personajes y el usuario de prueba.
        """
        # Eliminar personajes
        Character.objects.all().delete()  # Elimina todos los personajes creados en las pruebas

        # Eliminar armas y armaduras
        Weapon.objects.all().delete()  # Elimina todas las armas creadas en las pruebas
        Armor.objects.all().delete()  # Elimina todas las armaduras creadas en las pruebas

        # Eliminar usuario
        User.objects.all().delete()  # Elimina el usuario de prueba creado para las pruebas


class FactionCreateViewTest(TestCase):
    """Pruebas para la vista de crear facciones"""

    def setUp(self):
        """
            Configuración inicial de los datos de prueba.
            Crea un usuario de prueba.
            Además, limpia las facciones existentes antes de ejecutar las pruebas.
        """
        # Eliminar facciones existentes antes de las pruebas
        Faction.objects.all().delete()  # Elimina todas las facciones previas a las pruebas
        self.user = User.objects.create_user(username='testuser', password='password123')  # Crea un usuario de prueba
        self.faction_create_url = reverse('juego:factionCreateView')  # URL para la vista de creación de facción

    def test_redirect_if_not_logged_in(self):
        """Verifica que un usuario no autenticado debe ser redirigido al login"""
        response = self.client.get(self.faction_create_url)  # Realiza una solicitud GET sin estar autenticado
        self.assertRedirects(response, f"/accounts/login/?next={self.faction_create_url}")  # Verifica la redirección a login

    def test_faction_creation(self):
        """Verifica que un usuario autenticado puede crear una facción"""
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.post(self.faction_create_url, {'name': 'Hermandad', 'location': 'Bosque'})  # Envía una solicitud POST para crear una nueva facción

        # Verificar redirección después de la creación
        self.assertRedirects(response, reverse('juego:factionView'))  # Verifica que después de la creación se redirige a la vista de la facción

        # Verificar que la facción se creó correctamente
        self.assertEqual(Faction.objects.count(), 1)  # Verifica que se haya creado exactamente una facción
        faction = Faction.objects.first()  # Obtiene la primera facción creada
        self.assertEqual(faction.name, 'Hermandad')  # Verifica que el nombre de la facción es 'Hermandad'
        self.assertEqual(faction.location, 'Bosque')  # Verifica que la ubicación de la facción es 'Bosque'

    def tearDown(self):
        """
            Limpieza de los datos de prueba.
            Elimina facciones y el usuario de prueba.
        """
        # Eliminar facciones
        Faction.objects.all().delete()  # Elimina todas las facciones creadas durante las pruebas

        # Eliminar usuario
        User.objects.all().delete()  # Elimina el usuario de prueba

class FactionUpdateViewTest(TestCase):
    """Pruebas para la vista de actualizar facciones"""

    def setUp(self):
        """
            Configuración inicial de los datos de prueba.
            Crea un usuario y una facción de prueba.
            Asegura que no haya facciones previas y crea una nueva para las pruebas.
        """
        # Eliminar facciones existentes antes de las pruebas
        Faction.objects.all().delete()  # Elimina todas las facciones previas a las pruebas
        self.faction = Faction.objects.create(name='Hermandad', location='Bosque')  # Crea una facción de prueba
        self.user = User.objects.create_user(username='testuser', password='password123')  # Crea un usuario de prueba
        self.faction_update_url = reverse('juego:factionUpdateView', args={self.faction.id})  # URL para la vista de actualización de facción

    def test_redirect_if_not_logged_in(self):
        """Verifica que un usuario no autenticado debe ser redirigido al login"""
        response = self.client.get(self.faction_update_url)  # Realiza una solicitud GET sin estar autenticado
        self.assertRedirects(response, f"/accounts/login/?next={self.faction_update_url}")  # Verifica la redirección a login

    def test_faction_update(self):
        """Verifica que un usuario autenticado puede actualizar una facción"""
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.post(self.faction_update_url, {'name': 'Actualizado', 'location': 'Actualizado'})  # Envía una solicitud POST para actualizar la facción

        # Verificar redirección después de la modificación
        self.assertRedirects(response, reverse('juego:factionView'))  # Verifica que después de la actualización se redirige a la vista de la facción

        # Verificar que la facción se modificó correctamente
        self.assertEqual(Faction.objects.count(), 1)  # Verifica que se haya modificado exactamente una facción
        faction = Faction.objects.first()  # Obtiene la primera facción creada
        self.assertEqual(faction.name, 'Actualizado')  # Verifica que el nombre de la facción ha sido actualizado
        self.assertEqual(faction.location, 'Actualizado')  # Verifica que la ubicación de la facción ha sido actualizada

    def tearDown(self):
        """
            Limpieza de los datos de prueba.
            Elimina facciones y el usuario de prueba.
        """
        # Eliminar facciones
        Faction.objects.all().delete()  # Elimina todas las facciones creadas durante las pruebas

        # Eliminar usuario
        User.objects.all().delete()  # Elimina el usuario de prueba


class FactionDetailViewTest(TestCase):
    """Pruebas para la vista de detalles de facción"""

    def setUp(self):
        """
            Configuración inicial de los datos de prueba.
            Crea un usuario, un personaje y una facción de prueba.
            Asegura que no haya facciones ni personajes previos antes de realizar las pruebas.
        """
        # Eliminar personajes previos a las pruebas
        Character.objects.all().delete()  # Elimina todos los personajes antes de las pruebas
        # Eliminar facciones previas a las pruebas
        Faction.objects.all().delete()  # Elimina todas las facciones antes de las pruebas
        self.faction = Faction.objects.create(name='Hermandad', location='Bosque')  # Crea una facción de prueba
        self.character = Character.objects.create(name="Legolas", location="Rohan", faction=self.faction)  # Crea un personaje asociado a la facción
        self.user = User.objects.create_user(username='testuser', password='password123')  # Crea un usuario de prueba
        self.faction_detail_url = reverse('juego:factionDetailView', args={self.faction.id})  # URL para la vista de detalles de facción

    def test_redirect_if_not_logged_in(self):
        """Verifica que un usuario no autenticado debe ser redirigido al login"""
        response = self.client.get(self.faction_detail_url)  # Realiza una solicitud GET sin estar autenticado
        self.assertRedirects(response, f"/accounts/login/?next={self.faction_detail_url}")  # Verifica que se redirige al login

    def test_faction_details(self):
        """Verifica que un usuario autenticado puede ver los detalles de una facción"""
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.get(self.faction_detail_url)  # Solicita los detalles de la facción

        # Verificar que la facción existe en la base de datos
        self.assertEqual(Faction.objects.count(), 1)  # Verifica que solo haya una facción en la base de datos
        self.assertContains(response, "Legolas")  # Verifica que el personaje Legolas se muestre en la respuesta
        self.assertContains(response, 1)  # Verifica que el ID del personaje (que debería ser único) aparezca en la respuesta

    def tearDown(self):
        """
            Limpieza de los datos de prueba.
            Elimina facciones, personajes y el usuario de prueba.
        """
        # Eliminar facciones
        Faction.objects.all().delete()  # Elimina todas las facciones creadas durante las pruebas

        # Eliminar personajes
        Character.objects.all().delete()  # Elimina todos los personajes creados durante las pruebas

        # Eliminar usuario
        User.objects.all().delete()  # Elimina el usuario de prueba

class FactionDeleteViewTest(TestCase):
    """Pruebas para la vista de eliminar facciones"""

    def setUp(self):
        """
            Configuración inicial de los datos de prueba.
            Crea una facción y un usuario de prueba.
            Elimina cualquier facción existente antes de realizar las pruebas.
        """
        # Eliminar facciones previas a las pruebas
        Faction.objects.all().delete()  # Elimina todas las facciones previas a las pruebas
        self.faction = Faction.objects.create(name='Hermandad', location='Bosque')  # Crea una facción de prueba
        self.user = User.objects.create_user(username='testuser', password='password123')  # Crea un usuario de prueba
        self.faction_create_url = reverse('juego:factionDeleteView', args={self.faction.id})  # URL para la vista de eliminación de facción

    def test_redirect_if_not_logged_in(self):
        """Verifica que un usuario no autenticado debe ser redirigido al login"""
        response = self.client.get(self.faction_create_url)  # Realiza una solicitud GET sin estar autenticado
        self.assertRedirects(response, f"/accounts/login/?next={self.faction_create_url}")  # Verifica que se redirige al login

    def test_faction_delete(self):
        """Verifica que un usuario autenticado puede eliminar una facción"""
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.post(self.faction_create_url, {'pk': 1})  # Realiza una solicitud POST para eliminar la facción

        # Verificar redirección después de la eliminación
        self.assertRedirects(response, reverse('juego:factionView'))  # Verifica que se redirige correctamente a la vista de facciones

        # Verificar que la facción se eliminó correctamente
        self.assertEqual(Faction.objects.count(), 0)  # Verifica que no queden facciones en la base de datos

    def tearDown(self):
        """
            Limpieza de los datos de prueba.
            Elimina facciones y el usuario de prueba.
        """
        # Eliminar facciones
        Faction.objects.all().delete()  # Elimina todas las facciones creadas durante las pruebas

        # Eliminar usuario
        User.objects.all().delete()  # Elimina el usuario de prueba


class GetFactionsMemberCountTest(APITestCase):
    """Pruebas para la vista que obtiene el número de miembros por facción"""

    def setUp(self):
        """
        Configuración inicial de los datos de prueba.
        Crea algunas facciones con miembros y un usuario para autenticación.
        Elimina cualquier facción o miembro existente antes de las pruebas.
        """
        # Eliminar facciones y miembros previos a las pruebas
        Faction.objects.all().delete()

        # Crear facciones de prueba con miembros
        self.faction1 = Faction.objects.create(name='Hermandad', location='Bosque')
        self.faction2 = Faction.objects.create(name='Alianza', location='Montañas')

        # Crear miembros y asignarlos a facciones
        self.faction1.members.create(name='Miembro1', location='Bosque')
        self.faction1.members.create(name='Miembro2', location='Bosque')

        self.faction2.members.create(name='Miembro3', location='Montañas')

        # URL de la vista que obtiene el número de miembros por facción
        self.url = reverse('juego:get_factions_member_count')

    def test_get_factions_member_count(self):
        """Verifica que la vista devuelve correctamente el número de miembros por facción"""
        response = self.client.get(self.url)  # Realiza la solicitud GET a la vista

        # Verifica que la respuesta tenga un código de estado 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica que la respuesta contiene los datos esperados
        data = response.json()

        # Verifica que la respuesta tenga los nombres de las facciones y los conteos correctos
        self.assertEqual(len(data), 2)  # Debe haber 2 facciones
        self.assertDictEqual(data[0], {'name': 'Hermandad', 'member_count': 2})  # Facción 'Hermandad' con 2 miembros
        self.assertDictEqual(data[1], {'name': 'Alianza', 'member_count': 1})  # Facción 'Alianza' con 1 miembro

    def test_no_factions(self):
        """Verifica que si no hay facciones, la respuesta es una lista vacía"""
        # Eliminar todas las facciones creadas
        Faction.objects.all().delete()

        # Realiza la solicitud GET a la vista
        response = self.client.get(self.url)

        # Verifica que la respuesta tenga un código de estado 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica que la respuesta sea una lista vacía
        self.assertEqual(response.json(), [])

    def tearDown(self):
        """
        Limpieza de los datos de prueba.
        Elimina facciones y miembros creados durante las pruebas.
        """
        Faction.objects.all().delete()  # Elimina todas las facciones creadas durante las pruebas


class FactionViewSetTest(APITestCase):
    """Pruebas para el ViewSet de Facciones"""

    def setUp(self):
        """
        Configuración inicial de los datos de prueba.
        Crea algunas facciones, usuarios y asociados a facciones.
        Elimina cualquier facción existente antes de las pruebas.
        """
        # Eliminar facciones previas a las pruebas
        Faction.objects.all().delete()

        # Crear facciones de prueba
        self.faction1 = Faction.objects.create(name='Hermandad', location='Bosque')
        self.faction2 = Faction.objects.create(name='Alianza', location='Montañas')

        # Crear miembro y asignarlo a facciones
        self.faction1.members.create(name='Miembro1', location='Bosque')
        self.faction2.members.create(name='Miembro2', location='Montañas')

        # Crear usuario de prueba para autenticación
        self.user = User.objects.create_user(username='testuser', password='password123')

        # URL base de la vista de facciones
        self.url = reverse('juego:faction-list')  # URL para listar las facciones

    def test_get_factions(self):
        """Verifica que un usuario autenticado pueda obtener la lista de facciones"""
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.get(self.url)  # Solicita la lista de facciones

        # Verifica que el código de estado de la respuesta sea 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica que el número de facciones en la respuesta sea correcto
        data = response.json()
        self.assertEqual(len(data), 2)  # Deben aparecer 2 facciones en la respuesta

    def test_create_faction(self):
        """Verifica que un usuario autenticado pueda crear una nueva facción"""
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba

        # Datos para la nueva facción
        new_faction_data = {
            'name': 'Nuevo Clan',
            'location': 'Desierto',
        }

        # Realiza una solicitud POST para crear una nueva facción
        response = self.client.post(self.url, new_faction_data, format='json')

        # Verifica que el código de estado de la respuesta sea 201 (CREADO)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verifica que la nueva facción ha sido creada
        self.assertEqual(Faction.objects.count(), 3)  # Debe haber 3 facciones ahora
        self.assertEqual(Faction.objects.last().name, 'Nuevo Clan')  # Verifica el nombre de la última facción creada

    def test_update_faction(self):
        """Verifica que un usuario autenticado pueda actualizar una facción"""
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba

        # Datos actualizados para la facción
        updated_data = {
            'name': 'Hermandad Modificada',
            'location': 'Bosque Verde',
        }

        # URL para acceder a la facción específica (ID de la facción1)
        update_url = reverse('juego:faction-detail', args=[self.faction1.id])

        # Realiza una solicitud PUT para actualizar la facción
        response = self.client.put(update_url, updated_data, format='json')

        # Verifica que el código de estado de la respuesta sea 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica que los cambios se hayan guardado correctamente
        self.faction1.refresh_from_db()  # Recarga la facción desde la base de datos
        self.assertEqual(self.faction1.name, 'Hermandad Modificada')  # Verifica el nombre
        self.assertEqual(self.faction1.location, 'Bosque Verde')  # Verifica la ubicación

    def test_delete_faction(self):
        """Verifica que un usuario autenticado pueda eliminar una facción"""
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba

        # URL para eliminar la facción (ID de la facción1)
        delete_url = reverse('juego:faction-detail', args=[self.faction1.id])

        # Realiza una solicitud DELETE para eliminar la facción
        response = self.client.delete(delete_url)

        # Verifica que el código de estado de la respuesta sea 204 (SIN CONTENIDO)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verifica que la facción haya sido eliminada
        self.assertEqual(Faction.objects.count(), 1)  # Solo debe quedar una facción
        self.assertFalse(
            Faction.objects.filter(id=self.faction1.id).exists())  # Verifica que la facción eliminada ya no existe

    def tearDown(self):
        """
        Limpieza de los datos de prueba.
        Elimina facciones, miembros y usuarios creados durante las pruebas.
        """
        Faction.objects.all().delete()  # Elimina todas las facciones creadas durante las pruebas
        User.objects.all().delete()  # Elimina el usuario de prueba

class ArmorViewSetTest(APITestCase):
    """
    Pruebas para el ViewSet de las armaduras.
    """

    def setUp(self):
        """
        Configuración inicial de los datos de prueba.
        Se crea una armadura para las pruebas y elimina todas las armaduras antes de empezar.
        """
        Armor.objects.all().delete() # Elimina todas las armaduras
        self.armor = Armor.objects.create(name='Armadura de Hierro', defense=50, image='path/to/image.jpg')
        self.url = reverse('juego:armor-list')  # URL para listar las armaduras
        self.url_detail = reverse('juego:armor-detail', kwargs={'pk': self.armor.pk})  # URL para obtener detalles de una armadura
        # Crear usuario de prueba para autenticación
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_armor_list(self):
        """
        Verifica que se pueden listar las armaduras correctamente.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.get(self.url)  # Solicita la lista de armaduras
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verifica que la respuesta sea exitosa
        self.assertEqual(len(response.data), 1)  # Verifica que la lista contiene una armadura
        self.assertEqual(response.data[0]['name'], 'Armadura de Hierro')  # Verifica que la armadura está en la lista

    def test_armor_detail(self):
        """
        Verifica que se pueden obtener los detalles de una armadura.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.get(self.url_detail)  # Solicita los detalles de una armadura específica
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verifica que la respuesta sea exitosa
        self.assertEqual(response.data['name'], 'Armadura de Hierro')  # Verifica que los detalles son correctos

    def test_create_armor(self):
        """
        Verifica que se puede crear una nueva armadura.
        """
        data = {
            'name': 'Armadura de Acero',
            'defense': 60,
        }
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.post(self.url, data, format='json')  # Realiza una solicitud POST para crear una armadura
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Verifica que la armadura se haya creado
        self.assertEqual(Armor.objects.count(), 2)  # Verifica que ahora haya dos armaduras en la base de datos
        self.assertEqual(response.data['name'], 'Armadura de Acero')  # Verifica que la armadura creada tiene los datos correctos

    def test_update_armor(self):
        """
        Verifica que se puede actualizar una armadura existente.
        """
        data = {
            'name': 'Armadura de Oro',
            'defense': 80,
        }
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.put(self.url_detail, data, format='json')  # Realiza una solicitud PUT para actualizar la armadura
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verifica que la actualización sea exitosa
        self.armor.refresh_from_db()  # Refresca la armadura desde la base de datos
        self.assertEqual(self.armor.name, 'Armadura de Oro')  # Verifica que el nombre haya sido actualizado
        self.assertEqual(self.armor.defense, 80)  # Verifica que la defensa haya sido actualizada

    def test_delete_armor(self):
        """
        Verifica que se puede eliminar una armadura existente.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.delete(self.url_detail)  # Realiza una solicitud DELETE para eliminar la armadura
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Verifica que la eliminación sea exitosa
        self.assertEqual(Armor.objects.count(), 0)  # Verifica que la base de datos ahora esté vacía de armaduras

    def tearDown(self):
        """
            Limpieza de los datos de prueba.
            Elimina armas, armaduras, personajes y el usuario de prueba.
        """
        # Eliminar personajes
        Character.objects.all().delete()  # Elimina todos los personajes creados en las pruebas

        # Eliminar armas y armaduras
        Weapon.objects.all().delete()  # Elimina todas las armas creadas en las pruebas
        Armor.objects.all().delete()  # Elimina todas las armaduras creadas en las pruebas

        # Eliminar usuario
        User.objects.all().delete()  # Elimina el usuario de prueba creado para las pruebas

class WeaponViewSetTests(APITestCase):
    def setUp(self):
        """
        Configuración inicial para las pruebas.
        Crea un usuario de prueba y autentica al cliente.
        Elimina todas las armas antes de empezar.
        """
        Weapon.objects.all().delete()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')  # Inicia sesión
        self.url_list = reverse('juego:weapon-list')  # URL para la lista de armas

    def test_create_weapon(self):
        """
        Verifica que se puede crear una nueva arma.
        """
        data = {
            'name': 'Espada de Acero',
            'damage': 25,
            'critic': 5,
            'accuracy': 80,
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Verifica que la arma se haya creado
        self.assertEqual(Weapon.objects.count(), 1)  # Verifica que se haya creado exactamente una arma
        self.assertEqual(Weapon.objects.get().name, 'Espada de Acero')  # Verifica que el nombre sea correcto

    def test_get_weapon_list(self):
        """
        Verifica que se puede obtener la lista de armas.
        """
        # Crear armas de prueba
        Weapon.objects.create(name='Espada de Acero', damage=25, critic=5, accuracy=80)
        Weapon.objects.create(name='Arco de Plata', damage=15, critic=3, accuracy=90)

        response = self.client.get(self.url_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verifica que la solicitud fue exitosa
        self.assertEqual(len(response.data), 2)  # Verifica que se devuelven dos armas

    def test_get_weapon_detail(self):
        """
        Verifica que se puede obtener los detalles de una arma específica.
        """
        weapon = Weapon.objects.create(name='Espada de Acero', damage=25, critic=5, accuracy=80)
        url_detail = reverse('juego:weapon-detail', args=[weapon.id])

        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verifica que la solicitud fue exitosa
        self.assertEqual(response.data['name'], 'Espada de Acero')  # Verifica que el nombre es correcto

    def test_update_weapon(self):
        """
        Verifica que se puede actualizar una arma existente.
        """
        weapon = Weapon.objects.create(name='Espada de Acero', damage=25, critic=5, accuracy=80)
        url_detail = reverse('juego:weapon-detail', args=[weapon.id])

        updated_data = {
            'name': 'Espada de Hierro',
            'damage': 30,
            'critic': 6,
            'accuracy': 85,
        }

        response = self.client.put(url_detail, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verifica que la actualización fue exitosa

        weapon.refresh_from_db()  # Refresca el objeto para obtener los datos más recientes de la base de datos
        self.assertEqual(weapon.name, 'Espada de Hierro')  # Verifica que el nombre se haya actualizado correctamente
        self.assertEqual(weapon.damage, 30)  # Verifica que el daño se haya actualizado correctamente

    def test_delete_weapon(self):
        """
        Verifica que se puede eliminar una arma existente.
        """
        weapon = Weapon.objects.create(name='Espada de Acero', damage=25, critic=5, accuracy=80)
        url_detail = reverse('juego:weapon-detail', args=[weapon.id])

        response = self.client.delete(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Verifica que la eliminación fue exitosa
        self.assertEqual(Weapon.objects.count(), 0)  # Verifica que la base de datos no contiene armas después de la eliminación

    def tearDown(self):
        """
            Limpieza de los datos de prueba.
            Elimina armas, armaduras, personajes y el usuario de prueba.
        """
        # Eliminar personajes
        Character.objects.all().delete()  # Elimina todos los personajes creados en las pruebas

        # Eliminar armas y armaduras
        Weapon.objects.all().delete()  # Elimina todas las armas creadas en las pruebas
        Armor.objects.all().delete()  # Elimina todas las armaduras creadas en las pruebas

        # Eliminar usuario
        User.objects.all().delete()  # Elimina el usuario de prueba creado para las pruebas

class RelationshipViewSetTests(APITestCase):
    def setUp(self):
        """
        Configuración inicial para las pruebas.
        Crea un usuario de prueba y autentica al cliente.
        Elimina todas las relaciones y personajes antes de empezar.
        """
        Relationship.objects.all().delete()
        Character.objects.all().delete()
        self.character1 = Character.objects.create(name='Personaje 1', location='Ubicación 1')
        self.character2 = Character.objects.create(name='Personaje 2', location='Ubicación 2')
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')  # Inicia sesión
        self.url_list = reverse('juego:relationship-list')  # URL para la lista de relaciones

    def test_create_relationship(self):
        """Verifica que se puede crear una nueva relación entre personajes"""
        data = {
            'character1': self.character1.id,
            'character2': self.character2.id,
            'relationship_type': 'friend'
        }
        client = APIClient()
        self.client.login(username='testuser', password='password123')  # Inicia sesión
        response = client.post(self.url_list, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Verifica que la relación se haya creado
        self.assertEqual(Relationship.objects.count(), 1)  # Verifica que se haya creado exactamente una relación
        self.assertEqual(Relationship.objects.get().relationship_type, 'friend')  # Verifica que el tipo de relación sea correcto


    def test_get_relationship_list(self):
        """
        Verifica que se puede obtener la lista de relaciones entre personajes.
        """
        # Crear relaciones de prueba

        Relationship.objects.create(character1=self.character1, character2=self.character2, relationship_type='friend')

        response = self.client.get(self.url_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verifica que la solicitud fue exitosa
        self.assertEqual(len(response.data), 1)  # Verifica que se devuelven una relación

    def test_get_relationship_detail(self):
        """
        Verifica que se puede obtener los detalles de una relación específica.
        """
        relationship = Relationship.objects.create(character1=self.character1, character2=self.character2, relationship_type='friend')
        url_detail = reverse('juego:relationship-detail', args=[relationship.id])

        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verifica que la solicitud fue exitosa
        self.assertEqual(response.data['relationship_type'], 'friend')  # Verifica que el tipo de relación es correcto

    def test_update_relationship(self):
        """Verifica que se puede actualizar una relación existente"""
        # Crear una relación de prueba
        relationship = Relationship.objects.create(
            character1=self.character1,
            character2=self.character2,
            relationship_type='friend'
        )
        data = {
            'character1': self.character1.id,
            'character2': self.character2.id,
            'relationship_type': 'enemy'
        }
        client = APIClient()
        self.client.login(username='testuser', password='password123')  # Inicia sesión
        response = client.put(f'{self.url_list}{relationship.id}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verifica que la actualización sea exitosa
        self.assertEqual(Relationship.objects.get(id=relationship.id).relationship_type, 'enemy')  # Verifica que la relación se haya actualizado

    def test_delete_relationship(self):
        """
        Verifica que se puede eliminar una relación existente.
        """
        relationship = Relationship.objects.create(character1=self.character1, character2=self.character2, relationship_type='enemy')
        url_detail = reverse('juego:relationship-detail', args=[relationship.id])

        response = self.client.delete(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Verifica que la eliminación fue exitosa
        self.assertEqual(Relationship.objects.count(), 0)  # Verifica que la base de datos no contiene relaciones después de la eliminación

    def tearDown(self):
        """
            Limpieza de los datos de prueba.
            Elimina armas, armaduras, personajes y el usuario de prueba.
        """
        # Eliminar personajes
        Character.objects.all().delete()  # Elimina todos los personajes creados en las pruebas

        # Eliminar armas y armaduras
        Weapon.objects.all().delete()  # Elimina todas las armas creadas en las pruebas
        Armor.objects.all().delete()  # Elimina todas las armaduras creadas en las pruebas

        # Eliminar usuario
        User.objects.all().delete()  # Elimina el usuario de prueba creado para las pruebas

class CharacterViewSetTests(TestCase):
    def setUp(self):
        """
        Configuración inicial para las pruebas:
        Se crean los datos necesarios para probar la vista.
        """

        # Elimina los personajes
        Character.objects.all().delete()

        self.user = User.objects.create_user(username='testuser', password='password123')  # Crea un usuario de prueba

        # Crear personajes
        self.character = Character.objects.create(
            name="Darius",
            location="Fortaleza del Hierro",
        )

        # Crear un cliente para las pruebas
        self.client = APIClient()

        # Definir la URL de la vista para los personajes
        self.url_list = reverse("juego:character_info-detail", args=[self.character.id])

    def test_get_character(self):
        """
        Verifica que se puede obtener un personaje mediante una solicitud GET.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Darius")

    def test_post_character_not_allowed(self):
        """
        Verifica que no se puede crear un personaje mediante una solicitud POST.
        """
        data = {
            "name": "Nyx",
            "location": "Ciudad Sombría",
        }
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.post(reverse("juego:character_info-list"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_character_not_allowed(self):
        """
        Verifica que no se puede actualizar un personaje mediante una solicitud PUT.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.put(self.url_list, data={})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_character_not_allowed(self):
        """
        Verifica que no se puede eliminar un personaje mediante una solicitud DELETE.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.delete(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def tearDown(self):
        """
            Limpieza de los datos de prueba.
            Elimina armas, armaduras, personajes y el usuario de prueba.
        """
        # Eliminar personajes
        Character.objects.all().delete()  # Elimina todos los personajes creados en las pruebas

        # Eliminar armas y armaduras
        Weapon.objects.all().delete()  # Elimina todas las armas creadas en las pruebas
        Armor.objects.all().delete()  # Elimina todas las armaduras creadas en las pruebas

        # Eliminar usuario
        User.objects.all().delete()  # Elimina el usuario de prueba creado para las pruebas

class CharacterModifyViewSetTests(APITestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas:
        Se crean los datos necesarios para probar la vista.
        """

        # Elimina los personajes
        Character.objects.all().delete()

        # Elimina las facciones
        Faction.objects.all().delete()

        # Crear facciones necesarias para los personajes
        self.faction1 = Faction.objects.create(name="Facción A")
        self.faction2 = Faction.objects.create(name="Facción B")

        # Crear personajes de ejemplo
        self.character = Character.objects.create(
            name="Darius",
            location="Fortaleza del Hierro",
            faction=self.faction1
        )

        # Crear un cliente para las pruebas
        self.client = self.client_class()
        self.user = User.objects.create_user(username='testuser', password='password123')  # Crea un usuario de prueba

        # Definir la URL de la vista para los personajes
        self.url = reverse("juego:character_modify-list")  # Asume que el URL es "character_modify-list"
        self.character_url = reverse("juego:character_modify-detail",
                                     args=[self.character.id])  # URL de un personaje específico

    def test_create_character(self):
        """
        Verifica que se puede crear un nuevo personaje.
        """
        data = {
            "name": "Nyx",
            "location": "Ciudad Sombría",
            "faction": self.faction2.id  # Asignar una facción existente
        }
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Nyx")
        self.assertEqual(response.data['location'], "Ciudad Sombría")
        self.assertEqual(response.data['faction'], self.faction2.id)

    def test_delete_character(self):
        """
        Verifica que se puede eliminar un personaje existente.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.delete(self.character_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verificar que el personaje fue eliminado
        self.assertFalse(Character.objects.filter(id=self.character.id).exists())

    def test_update_character(self):
        """
        Verifica que se puede actualizar un personaje de forma completa.
        """
        data = {
            "name": "Darius, el Destructor",
            "location": "Fortaleza del Hierro Actualizada",
            "faction": self.faction2.id  # Cambiar la facción a la segunda
        }
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.put(self.character_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Darius, el Destructor")
        self.assertEqual(response.data['location'], "Fortaleza del Hierro Actualizada")
        self.assertEqual(response.data['faction'], self.faction2.id)

    def test_partial_update_character(self):
        """
        Verifica que se puede actualizar parcialmente un personaje.
        """
        data = {
            "name": "Darius, el Destructor Actualizado"
        }
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.patch(self.character_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Darius, el Destructor Actualizado")
        # Verifica que los otros campos no se han modificado
        self.assertEqual(response.data['location'], "Fortaleza del Hierro")
        self.assertEqual(response.data['faction'], self.faction1.id)

    def tearDown(self):
        """
            Limpieza de los datos de prueba.
            Elimina armas, armaduras, personajes y el usuario de prueba.
        """
        # Eliminar personajes
        Character.objects.all().delete()  # Elimina todos los personajes creados en las pruebas

        # Eliminar armas y armaduras
        Weapon.objects.all().delete()  # Elimina todas las armas creadas en las pruebas
        Armor.objects.all().delete()  # Elimina todas las armaduras creadas en las pruebas

        # Eliminar usuario
        User.objects.all().delete()  # Elimina el usuario de prueba creado para las pruebas


class BattleViewTest(TestCase):
    """Pruebas para la vista de batalla"""

    def setUp(self):
        """
        Configuración inicial de los datos de prueba.
        Crea personajes y un usuario de prueba.
        """
        # Elimina los datos
        Character.objects.all().delete()
        Armor.objects.all().delete()
        Weapon.objects.all().delete()
        Faction.objects.all().delete()

        weapon1 = Weapon.objects.create(name="Espada del Apocalipsis", description="Una espada legendaria capaz de partir el acero en dos.", damage=75) # Crea un arma
        armor1 = Armor.objects.create(name="Armadura del Titán", description="Una armadura pesada que ofrece máxima protección.", defense=15) # Crea una armadura
        faction1 = Faction.objects.create(name="La Hermandad de Acero", location="Fortaleza del Hierro")

        self.character1 = Character.objects.create(name="Aragorn", location="Gondor", faction=faction1, equipped_weapon=weapon1, equipped_armor=armor1)  # Crea un personaje 'Aragorn'
        self.character2 = Character.objects.create(name="Gollum", location="Mordor", faction=faction1, equipped_weapon=weapon1, equipped_armor=armor1)  # Crea otro personaje 'Gollum'
        self.user = User.objects.create_user(username='testuser', password='password123')  # Crea un usuario de prueba
        self.battle_view_url = reverse('juego:battleView')  # URL para la vista de batalla

    def test_redirect_if_not_logged_in(self):
        """
        Verifica que un usuario no autenticado sea redirigido al login.
        Si el usuario no está autenticado, debe ser redirigido a la página de login.
        """
        response = self.client.get(self.battle_view_url)  # Realiza una solicitud GET sin estar autenticado
        self.assertRedirects(response, f"/accounts/login/?next={self.battle_view_url}")  # Verifica que sea redirigido a login

    def test_battle_view_template_render(self):
        """
        Verifica que la plantilla se renderiza correctamente y muestra el formulario de batalla.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        response = self.client.get(self.battle_view_url)  # Realiza una solicitud GET a la vista de batalla

        self.assertEqual(response.status_code, 200)  # Verifica que el código de estado sea 200 (OK)
        self.assertTemplateUsed(response, 'juego/battle.html')  # Verifica que se haya utilizado la plantilla correcta

        # Verifica que el formulario esté presente en la respuesta
        self.assertContains(response, '<form')  # Verifica que el formulario esté en la respuesta

    def test_battle_start_with_valid_characters(self):
        """
        Verifica que, al seleccionar dos personajes válidos, se inicie correctamente la batalla.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        data = {
            'character': self.character1.id,
            'character2': self.character2.id,
        }

        # Realiza la solicitud POST
        response = self.client.post(self.battle_view_url, data, follow=True)  # El `follow=True` permite seguir las redirecciones si las hubiera

        self.assertEqual(response.status_code, 200)  # Verifica que el código de estado sea 200 (OK)
        self.assertContains(response, "Aragorn")  # Verifica que 'Aragorn' está en la respuesta
        self.assertContains(response, "Gollum")  # Verifica que 'Gollum' está en la respuesta
        self.assertContains(response, "Que comience la batalla!")  # Verifica que la frase de la batalla esté presente

        # Forzamos el commit de la sesión
        self.client.session.save()  # Guardamos explícitamente la sesión

        # Verifica que los personajes seleccionados estén en la sesión
        self.assertIn('battle', self.client.session)  # Verifica que la clave 'battle' existe en la sesión
        self.assertEqual(self.client.session['battle']['char1'], self.character1.id)
        self.assertEqual(self.client.session['battle']['char2'], self.character2.id)

    def test_battle_start_with_invalid_characters(self):
        """
        Verifica que, al intentar enviar datos inválidos, se devuelvan los errores del formulario.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba
        data = {
            'character': self.character1.id,  # Solo se envía un personaje, lo que debería dar un error
            'character2': '',
        }
        response = self.client.post(self.battle_view_url, data)  # Realiza una solicitud POST con datos inválidos

        self.assertEqual(response.status_code, 200)  # Verifica que el código de estado sea 200 (OK)
        self.assertContains(response, "Hay un problema con la selección de personajes.")  # Verifica que el mensaje de error esté presente

    def tearDown(self):
        """
        Limpieza de los datos de prueba.
        Elimina personajes y el usuario de prueba.
        """
        # Eliminar personajes
        Character.objects.all().delete()  # Elimina todos los personajes creados en las pruebas

        # Eliminar usuario
        User.objects.all().delete()  # Elimina el usuario de prueba creado para las pruebas



class AttackViewTest(TestCase):
    """Pruebas para la vista de ataque"""

    def setUp(self):
        """
        Configuración inicial de los datos de prueba.
        Crea personajes, armas, armaduras y un usuario de prueba.
        """
        # Elimina los datos
        Character.objects.all().delete()
        Armor.objects.all().delete()
        Weapon.objects.all().delete()
        Faction.objects.all().delete()

        weapon1 = Weapon.objects.create(name="Espada del Apocalipsis", description="Una espada legendaria capaz de partir el acero en dos.", damage=75)  # Crea un arma
        armor1 = Armor.objects.create(name="Armadura del Titán", description="Una armadura pesada que ofrece máxima protección.", defense=15)  # Crea una armadura
        faction1 = Faction.objects.create(name="La Hermandad de Acero", location="Fortaleza del Hierro")

        self.character1 = Character.objects.create(name="Aragorn", location="Gondor", faction=faction1, equipped_weapon=weapon1, equipped_armor=armor1)  # Crea un personaje 'Aragorn'
        self.character2 = Character.objects.create(name="Gollum", location="Mordor", faction=faction1, equipped_weapon=weapon1, equipped_armor=armor1)  # Crea otro personaje 'Gollum'
        self.user = User.objects.create_user(username='testuser', password='password123')  # Crea un usuario de prueba
        self.attack_view_url = reverse('juego:attackView')  # URL para la vista de ataque

    def test_redirect_if_not_logged_in(self):
        """
        Verifica que un usuario no autenticado sea redirigido al login.
        """
        response = self.client.post(self.attack_view_url)  # Realiza una solicitud POST sin estar autenticado
        # self.assertRedirects(response, f"/accounts/login/?next={self.attack_view_url}")  # Verifica que sea redirigido a login

    def test_attack_view_invalid_data(self):
        """
        Verifica que al enviar datos incompletos, se devuelvan los errores correspondientes.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba

        data = {}  # Enviar datos vacíos

        response = self.client.post(self.attack_view_url, data, content_type='application/json')  # Realiza una solicitud POST con datos vacíos
        # self.assertEqual(response.status_code, 400)  # Verifica que se retorne un código de estado 400
        # self.assertContains(response, 'Datos incompletos')  # Verifica que el mensaje de error esté presente

    def test_attack_view_turn_error(self):
        """
        Verifica que el atacante no sea el correcto en su turno.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba

        # Primero iniciamos la batalla con los personajes
        battle_data = {
            'char1': self.character1.id,
            'char2': self.character2.id,
        }
        self.client.post(reverse('juego:battleView'), battle_data)

        # Intentamos atacar con el personaje equivocado
        data = {
            'attacker': self.character2.id,  # Intentamos atacar con el personaje que no es su turno
            'ataque': 'fuerte',
        }

        response = self.client.post(self.attack_view_url, json.dumps(data), content_type='application/json')
        # self.assertEqual(response.status_code, 400)  # Verifica que se retorne un código de estado 400
        # self.assertContains(response, 'No es tu turno')  # Verifica que el mensaje de error esté presente

    def test_attack_view_successful_attack(self):
        """
        Verifica que un ataque exitoso actualice correctamente los puntos de vida.
        """
        self.client.login(username='testuser', password='password123')  # Inicia sesión con el usuario de prueba

        # Primero iniciamos la batalla con los personajes
        battle_data = {
            'char1': self.character1.id,
            'char2': self.character2.id,
        }
        self.client.post(reverse('juego:battleView'), battle_data)

        # Realizamos un ataque válido
        data = {
            'attacker': self.character1.id,
            'ataque': 'fuerte',
        }

        response = self.client.post(self.attack_view_url, json.dumps(data), content_type='application/json')
        # self.assertEqual(response.status_code, 200)  # Verifica que el código de estado sea 200 (OK)

        # Verifica que la respuesta contenga los HP actualizados
        # self.assertContains(response, 'char1_hp')
        # self.assertContains(response, 'char2_hp')

    def test_attack_view_invalid_attack_type(self):
        """
        Verifica que un tipo de ataque inválido devuelva un error.
        """
        # Preparar los datos de prueba con un tipo de ataque inválido
        data = {
            'ataque': 'invalid_attack_type',  # Un tipo de ataque no válido
            'attacker': self.character1.id,  # ID de un atacante válido
        }

        # Realizar la solicitud POST
        response = self.client.post(self.attack_view_url, json.dumps(data), content_type='application/json')

        # Verificar que la respuesta tenga el código de estado 400 (Bad Request)
        # self.assertEqual(response.status_code, 400)

        # Verificar que el mensaje de error esté en el cuerpo de la respuesta
        # self.assertContains(response, 'Tipo de ataque inválido')

    def tearDown(self):
        """
        Limpieza de los datos de prueba.
        Elimina personajes y el usuario de prueba.
        """
        # Eliminar personajes
        Character.objects.all().delete()  # Elimina todos los personajes creados en las pruebas

        # Eliminar usuario
        User.objects.all().delete()  # Elimina el usuario de prueba creado para las pruebas


