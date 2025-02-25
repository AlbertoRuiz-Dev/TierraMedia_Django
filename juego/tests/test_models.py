from django.test import TestCase
from juego.models import Faction, Weapon, Armor, Character, Inventory, Relationship

class FactionModelTest(TestCase):
    def setUp(self):
        self.faction = Faction.objects.create(name="Héroes", location="Tierra Media")

    def test_faction_str(self):
        self.assertEqual(str(self.faction), "Héroes (Tierra Media)")

class WeaponModelTest(TestCase):
    def setUp(self):
        self.weapon = Weapon.objects.create(name="Espada", description="Espada de acero", damage=15)

    def test_weapon_str(self):
        self.assertEqual(str(self.weapon), "Espada (Daño: 15)")

    def test_default_description(self):
        weapon = Weapon.objects.create(name="Cuchillo")
        self.assertEqual(weapon.description, "Tan vago como siempre... sin descripción")

class ArmorModelTest(TestCase):
    def setUp(self):
        self.armor = Armor.objects.create(name="Cota de malla", description="Cota resistente", defense=10)

    def test_armor_str(self):
        self.assertEqual(str(self.armor), "Cota de malla (Defensa: 10)")

    def test_default_description(self):
        armor = Armor.objects.create(name="Escudo")
        self.assertEqual(armor.description, "Tan vago como siempre... sin descripción")

class CharacterModelTest(TestCase):
    def setUp(self):
        self.faction = Faction.objects.create(name="Villanos", location="Mordor")
        self.weapon = Weapon.objects.create(name="Maza", description="Maza pesada", damage=20)
        self.armor = Armor.objects.create(name="Armadura de hierro", description="Armadura resistente", defense=30)
        self.character = Character.objects.create(
            name="Sauron",
            location="Mordor",
            faction=self.faction,
            equipped_weapon=self.weapon,
            equipped_armor=self.armor
        )

    def test_character_str(self):
        self.assertEqual(str(self.character), "Sauron (Villanos) - Ubicación: Mordor")

    def test_character_equipment(self):
        self.assertEqual(self.character.equipped_weapon, self.weapon)
        self.assertEqual(self.character.equipped_armor, self.armor)

class InventoryModelTest(TestCase):
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

    def test_inventory_str(self):
        self.assertEqual(str(self.inventory), "Equipo de Legolas, Armas: ['Arco', 'Espada corta'], Armadura: ['Armadura ligera', 'Armadura pesada']")

    def test_inventory_weapons(self):
        self.assertEqual(list(self.inventory.weapons.all()), [self.weapon1, self.weapon2])

    def test_inventory_armors(self):
        self.assertEqual(list(self.inventory.armors.all()), [self.armor1, self.armor2])

class RelationshipModelTest(TestCase):
    def setUp(self):
        self.char1 = Character.objects.create(name="Aragorn", location="Gondor")
        self.char2 = Character.objects.create(name="Legolas", location="Mirkwood")

    def test_create_relationship(self):
        relationship = Relationship.objects.create(character1=self.char1, character2=self.char2, relationship_type='friend')
        self.assertEqual(relationship.character2, self.char2)
        self.assertEqual(relationship.relationship_type, 'friend')

    def test_access_relationships(self):
        relationship = Relationship.objects.create(character1=self.char1, character2=self.char2, relationship_type='ally')
        relationships = self.char1.relationships1.all()
        self.assertEqual(relationships.count(), 1)
        self.assertEqual(relationships.first(), relationship)