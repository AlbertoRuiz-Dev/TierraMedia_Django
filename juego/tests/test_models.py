from django.test import TestCase
from juego.models import Faction, Weapon, Armor, Character, Inventory, Relationship

class FactionModelTest(TestCase):
    def setUp(self):
        """
        Configura los datos de prueba, creando una facción 'Héroes' en 'Tierra Media'
        """
        # Se crea una facción llamada 'Héroes' en la ubicación 'Tierra Media'
        self.faction = Faction.objects.create(name="Héroes", location="Tierra Media")

    def test_faction_str(self):
        """
        Verifica que la representación en cadena de la facción sea 'Héroes (Tierra Media)'
        """
        # Se verifica que la representación en cadena de la facción sea la esperada
        self.assertEqual(str(self.faction), "Héroes (Tierra Media)")

class WeaponModelTest(TestCase):
    def setUp(self):
        """
        Configura los datos de prueba, creando un arma 'Espada' con descripción y daño especificados
        """
        # Se crea un arma llamada 'Espada' con una descripción y daño definidos
        self.weapon = Weapon.objects.create(name="Espada", description="Espada de acero", damage=15)

    def test_weapon_str(self):
        """
        Verifica que la representación en cadena del arma sea 'Espada (Daño: 15)'
        """
        # Se verifica que la representación en cadena del arma sea la esperada
        self.assertEqual(str(self.weapon), "Espada (Daño: 15)")

    def test_default_description(self):
        """
        Verifica que el campo descripción tenga el valor por defecto si no se proporciona una descripción
        """
        # Se crea un arma sin descripción y se verifica que se le asigne la descripción por defecto
        weapon = Weapon.objects.create(name="Cuchillo")
        self.assertEqual(weapon.description, "Tan vago como siempre... sin descripción")

class ArmorModelTest(TestCase):
    def setUp(self):
        """
        Configura los datos de prueba, creando una armadura 'Cota de malla' con descripción y defensa especificadas
        """
        # Se crea una armadura llamada 'Cota de malla' con una descripción y defensa definidos
        self.armor = Armor.objects.create(name="Cota de malla", description="Cota resistente", defense=10)

    def test_armor_str(self):
        """
        Verifica que la representación en cadena de la armadura sea 'Cota de malla (Defensa: 10)'
        """
        # Se verifica que la representación en cadena de la armadura sea la esperada
        self.assertEqual(str(self.armor), "Cota de malla (Defensa: 10)")

    def test_default_description(self):
        """
        Verifica que el campo descripción tenga el valor por defecto si no se proporciona una descripción
        """
        # Se crea una armadura sin descripción y se verifica que se le asigne la descripción por defecto
        armor = Armor.objects.create(name="Escudo")
        self.assertEqual(armor.description, "Tan vago como siempre... sin descripción")

class CharacterModelTest(TestCase):
    def setUp(self):
        """
        Configura los datos de prueba, creando una facción 'Villanos', un arma y una armadura para un personaje
        """
        # Se crea una facción llamada 'Villanos' en la ubicación 'Mordor'
        self.faction = Faction.objects.create(name="Villanos", location="Mordor")
        # Se crea un arma llamada 'Maza' con una descripción y daño definidos
        self.weapon = Weapon.objects.create(name="Maza", description="Maza pesada", damage=20)
        # Se crea una armadura llamada 'Armadura de hierro' con una descripción y defensa definidos
        self.armor = Armor.objects.create(name="Armadura de hierro", description="Armadura resistente", defense=30)
        # Se crea un personaje llamado 'Sauron', ubicado en 'Mordor', con la facción y equipo asignados
        self.character = Character.objects.create(
            name="Sauron",
            location="Mordor",
            faction=self.faction,
            equipped_weapon=self.weapon,
            equipped_armor=self.armor
        )

    def test_character_str(self):
        """
        Verifica que la representación en cadena del personaje sea 'Sauron (Villanos) - Ubicación: Mordor'
        """
        # Se verifica que la representación en cadena del personaje sea la esperada
        self.assertEqual(str(self.character), "Sauron (Villanos)")

    def test_character_equipment(self):
        """
        Verifica que el personaje tenga equipada la arma y armadura correctas
        """
        # Se verifica que el personaje tenga el arma y armadura correctas equipadas
        self.assertEqual(self.character.equipped_weapon, self.weapon)
        self.assertEqual(self.character.equipped_armor, self.armor)

class InventoryModelTest(TestCase):
    def setUp(self):
        """
        Configura los datos de prueba, creando un inventario con armas y armaduras para un personaje
        """
        # Se crea una facción llamada 'Aliados' en la ubicación 'Rohan'
        self.faction = Faction.objects.create(name="Aliados", location="Rohan")
        # Se crean dos armas llamadas 'Arco' y 'Espada corta' con sus descripciones y daño definidos
        self.weapon1 = Weapon.objects.create(name="Arco", description="Arco largo", damage=12)
        self.weapon2 = Weapon.objects.create(name="Espada corta", description="Espada afilada", damage=8)
        # Se crean dos armaduras llamadas 'Armadura ligera' y 'Armadura pesada' con sus descripciones y defensa definidas
        self.armor1 = Armor.objects.create(name="Armadura ligera", description="Armadura de cuero", defense=5)
        self.armor2 = Armor.objects.create(name="Armadura pesada", description="Armadura de placas", defense=15)
        # Se crea un personaje llamado 'Legolas' ubicado en 'Rohan' con la facción asignada
        self.character = Character.objects.create(name="Legolas", location="Rohan", faction=self.faction)
        # Se crea un inventario para el personaje, asignando las armas y armaduras creadas
        self.inventory = Inventory.objects.create(character=self.character)
        self.inventory.weapons.add(self.weapon1, self.weapon2)
        self.inventory.armors.add(self.armor1, self.armor2)

    def test_inventory_str(self):
        """
        Verifica que la representación en cadena del inventario incluya las armas y armaduras correctas
        """
        # Se verifica que la representación en cadena del inventario sea la esperada
        self.assertEqual(str(self.inventory), "Equipo de Legolas, Armas: ['Arco', 'Espada corta'], Armadura: ['Armadura ligera', 'Armadura pesada']")

    def test_inventory_weapons(self):
        """
        Verifica que el inventario contenga las armas correctas
        """
        # Se verifica que el inventario contenga las armas correctas
        self.assertEqual(list(self.inventory.weapons.all()), [self.weapon1, self.weapon2])

    def test_inventory_armors(self):
        """
        Verifica que el inventario contenga las armaduras correctas
        """
        # Se verifica que el inventario contenga las armaduras correctas
        self.assertEqual(list(self.inventory.armors.all()), [self.armor1, self.armor2])

class RelationshipModelTest(TestCase):
    def setUp(self):
        """
        Configura los datos de prueba, creando dos personajes para probar las relaciones entre ellos
        """
        # Se crean dos personajes llamados 'Aragorn' y 'Legolas', ubicados en 'Gondor' y 'Mirkwood'
        self.char1 = Character.objects.create(name="Aragorn", location="Gondor")
        self.char2 = Character.objects.create(name="Legolas", location="Mirkwood")

    def test_create_relationship(self):
        """
        Verifica que una relación entre dos personajes sea creada correctamente
        """
        # Se crea una relación entre 'Aragorn' y 'Legolas' con tipo 'friend'
        relationship = Relationship.objects.create(character1=self.char1, character2=self.char2, relationship_type='friend')
        # Se verifica que la relación se haya creado correctamente
        self.assertEqual(relationship.character2, self.char2)
        self.assertEqual(relationship.relationship_type, 'friend')

    def test_access_relationships(self):
        """
        Verifica que se puedan acceder a las relaciones de un personaje correctamente
        """
        # Se crea una relación entre 'Aragorn' y 'Legolas' con tipo 'ally'
        relationship = Relationship.objects.create(character1=self.char1, character2=self.char2, relationship_type='ally')
        # Se verifica que las relaciones de 'Aragorn' se puedan acceder correctamente
        relationships = self.char1.relationships1.all()
        self.assertEqual(relationships.count(), 1)
        self.assertEqual(relationships.first(), relationship)
