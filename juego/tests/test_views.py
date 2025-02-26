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

