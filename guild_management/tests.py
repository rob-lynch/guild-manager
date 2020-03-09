from django.test import TestCase
from guild_management.models import *

#Define the common setups shared among tests
def realmGuildSetup(self):
    Realm.objects.create(name='TestRealm')
    realm = Realm.objects.get(name='TestRealm')
    Guild.objects.create(name='TestGuild', realm=realm)

def characterSetup(self):
    realmGuildSetup(self)
    guild = Guild.objects.get(name='TestGuild')

    Rank.objects.create(name='TestRank')
    rank = Rank.objects.get(name='TestRank')

    Race.objects.create(name='TestRace')
    race = Race.objects.get(name='TestRace')

    PlayableClass.objects.create(name='TestClass')
    playable_class = PlayableClass.objects.get(name='TestClass')

    Character.objects.create(
        name='TestCharacter',
        playable_class=playable_class,
        rank=rank,
        race=race,
        guild=guild,
    )

def instanceSetup(self):
    Instance.objects.create(name='TestInstance',dkp=0)

def npcSetup(self):
    instanceSetup(self)
    instance = Instance.objects.get(name='TestInstance')

    Npc.objects.create(
        name='TestNpc',
        instance = instance,
        instance_appearance_order=1
    )

def raidSetup(self):
    characterSetup(self)
    npcSetup(self)
    instance = Instance.objects.get(name='TestInstance')

    Raid.objects.create(
        instance=instance,
        instance_date='2020-01-01',
        required=True
    )

def lootSetup(self):
    raidSetup(self)
    raid = Raid.objects.get(instance__name='TestInstance')
    character = Character.objects.get(name='TestCharacter')
    boss = Npc.objects.get(name='TestNpc')

    Item.objects.create(name='TestItem')
    item = Item.objects.get(name='TestItem')

    Loot.objects.create(
        character=character, 
        raid=raid, 
        item=item,
        boss=boss,
        priority=True,
        exceptional=True,
        notes='TestNotes',
    )

def attendanceSetup(self):
    raidSetup(self)
    raid = Raid.objects.get(instance__name='TestInstance')
    character = Character.objects.get(name='TestCharacter')

    Attendance.objects.create(
        raid_character=character,
        raid=raid
    )

class RealmGuildTestCase(TestCase):
    def setUp(self):
        realmGuildSetup(self)

    def test_guild_and_realm_names_are_returned(self):
        """The expected names of the Guild and associated Realm are returned"""
        guild = Guild.objects.get(name='TestGuild')
        realm = Realm.objects.get(name='TestRealm')

        self.assertEqual(str(realm), 'TestRealm')
        self.assertEqual(str(guild), 'TestGuild')
        self.assertEqual(guild.realm.name, 'TestRealm')

class CharacterTestCase(TestCase):
    def setUp(self):
        characterSetup(self)

    def test_rank_name_is_returned(self):
        """The expected Rank name is returned"""
        rank = Rank.objects.get(name='TestRank')
        self.assertEqual(str(rank), 'TestRank')

    def test_playable_class_name_is_returned(self):
        """The expected Playable Class name is returned"""
        playable_class = PlayableClass.objects.get(name='TestClass')
        self.assertEqual(str(playable_class), 'TestClass')
    
    def test_race_name_is_returned(self):
        """The expected Race name is returned"""
        race = Race.objects.get(name='TestRace')
        self.assertEqual(str(race), 'TestRace')

    def test_character_name_is_returned(self):
        """Test expected Character name is returned"""
        character = Character.objects.get(name='TestCharacter')
        self.assertEqual(str(character), 'TestCharacter')

class InstanceTestCase(TestCase):
    def setUp(self):
        instanceSetup(self)
    def test_instance_name_is_returned(self):
        """The expected instance name is returned"""
        instance = Instance.objects.get(name='TestInstance')
        self.assertEqual(str(instance), 'TestInstance')

class NpcTestCase(TestCase):
    def setUp(self):
        npcSetup(self)
    def test_instance_name_is_returned(self):
        """The expected NPC name is returned"""
        npc = Npc.objects.get(name='TestNpc')
        self.assertEqual(str(npc), 'TestNpc')

class RaidTestCase(TestCase):
    def setUp(self):
        raidSetup(self)
    def test_raid_name_is_returned(self):
        """The expected Raid name is returned"""
        raid = Raid.objects.get(instance__name='TestInstance')
        self.assertEqual(str(raid), 'January 1, 2020 - TestInstance')

class LootTestCase(TestCase):
    def setUp(self):
        lootSetup(self)

    def test_item_name_is_returned(self):
        """The expected item name is returned from the Loot and Item models"""
        loot = Loot.objects.get(item__name='TestItem')
        item = Item.objects.get(name='TestItem')

        self.assertEqual(str(loot), 'TestItem')
        self.assertEqual(str(item), 'TestItem')
        self.assertEqual(loot.item.name, 'TestItem')

class AttendanceTestCase(TestCase):
    def setUp(self):
        attendanceSetup(self)
    
    def test_attendance_name_is_returned(self):
        """The expected attendance name is returned"""
        attendance = Attendance.objects.get(raid__instance__name='TestInstance')
        self.assertEqual(str(attendance), '2020-01-01 - TestInstance: TestCharacter')
        
    