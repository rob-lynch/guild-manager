from django.test import TestCase
from guild_management.models import *
from guild_management.admin import *
from django.contrib.admin.sites import AdminSite


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

    #Create a main
    Character.objects.create(
        name='TestCharacterMain1',
        playable_class=playable_class,
        rank=rank,
        race=race,
        guild=guild,
        guild_join_date='2020-01-01',
        raid_eligibility_date='2020-01-15',
        eligible_raids_override=0,
        attended_raids_override=0,
        active=True
    )

    main_character = Character.objects.get(name='TestCharacterMain1')
    
    #Create an alt
    Character.objects.create(
        name='TestCharacterAlt1',
        playable_class=playable_class,
        rank=rank,
        race=race,
        guild=guild,
        guild_join_date='2020-02-01',
        raid_eligibility_date='2020-02-15',
        eligible_raids_override=0,
        attended_raids_override=0,
        active=True,
        main_character=main_character,
    )

    #Create another alt
    Character.objects.create(
        name='TestCharacterAlt2',
        playable_class=playable_class,
        rank=rank,
        race=race,
        guild=guild,
        guild_join_date='2020-02-01',
        eligible_raids_override=0,
        attended_raids_override=0,
        active=True,
        main_character=main_character,
    )

    #And another
    Character.objects.create(
        name='TestCharacterAlt3',
        playable_class=playable_class,
        rank=rank,
        race=race,
        guild=guild,
        guild_join_date='2020-03-01',
        raid_eligibility_date='2020-03-01',
        eligible_raids_override=0,
        attended_raids_override=0,
        active=True,
        main_character=main_character,
    )

    Character.objects.create(
        name='TestCharacterMain2',
        playable_class=playable_class,
        rank=rank,
        race=race,
        guild=guild,
        guild_join_date='2020-03-01',
        raid_eligibility_date='2020-03-15',
        eligible_raids_override=4,
        attended_raids_override=5,
        active=True
    )

    Character.objects.create(
        name='TestCharacterMain3',
        playable_class=playable_class,
        rank=rank,
        race=race,
        guild=guild,
        guild_join_date='2020-03-01',
        raid_eligibility_date='2020-03-15',
        eligible_raids_override=5,
        attended_raids_override=4,
        active=True
    )
    
def instanceSetup(self):
    instances = ['TestInstance1','TestInstance2','TestInstance3']
    
    for instance in instances:
        Instance.objects.create(name=instance,dkp=0)
    
def npcSetup(self):
    instanceSetup(self)
    instance = Instance.objects.get(name='TestInstance1')

    Npc.objects.create(
        name='TestNpc',
        instance = instance,
        instance_appearance_order=1
    )

def raidSetup(self):
    characterSetup(self)
    npcSetup(self)

    instance_first = Instance.objects.get(name='TestInstance1')
    instance_second = Instance.objects.get(name='TestInstance2')
    instance_third = Instance.objects.get(name='TestInstance3')

    Raid.objects.create(
        instance=instance_first,
        instance_date='2020-01-01',
        required=True
    )

    Raid.objects.create(
        instance=instance_second,
        instance_date='2020-01-15',
        required=False
    )

    Raid.objects.create(
        instance=instance_third,
        instance_date='2020-02-01',
        required=True
    )

def lootSetup(self):
    raidSetup(self)
    raid = Raid.objects.get(instance__name='TestInstance1')
    character = Character.objects.get(name='TestCharacterMain1')
    boss = Npc.objects.get(name='TestNpc')

    Item.objects.create(name='TestItem1')
    item_one = Item.objects.get(name='TestItem1')

    Item.objects.create(
        name='TestItem2',
        item_id=1234,
    )
    
    item_two = Item.objects.get(name='TestItem2')

    Loot.objects.create(
        character=character, 
        raid=raid, 
        item=item_one,
        boss=boss,
        priority=True,
        exceptional=True,
        notes='TestNotes',
    )

    Loot.objects.create(
        character=character, 
        raid=raid, 
        item=item_two,
        boss=boss,
        priority=False,
        exceptional=False,
    )


def attendanceSetup(self):
    raidSetup(self)
    characters = ['TestCharacterMain1','TestCharacterAlt1','TestCharacterAlt2']
    instances = ['TestInstance1','TestInstance2','TestInstance3']
    
    for instance in instances:
        raid = Raid.objects.get(instance__name=instance)
        character = Character.objects.get(name=characters[0])
        Attendance.objects.create(
            raid_character=character,
            raid=raid
        )
    
    raid = Raid.objects.get(instance__name=instances[1])
    character = Character.objects.get(name=characters[1])
    Attendance.objects.create(
        raid_character=character,
        raid=raid
    )

    raid = Raid.objects.get(instance__name=instances[2])
    character = Character.objects.get(name=characters[2])
    Attendance.objects.create(
        raid_character=character,
        raid=raid
    )

class RealmGuildModelTestCase(TestCase):
    def setUp(self):
        realmGuildSetup(self)

    def test_guild_and_realm_names_are_returned(self):
        """The expected names of the Guild and associated Realm are returned"""
        guild = Guild.objects.get(name='TestGuild')
        realm = Realm.objects.get(name='TestRealm')

        self.assertEqual(str(realm), 'TestRealm')
        self.assertEqual(str(guild), 'TestGuild')
        self.assertEqual(guild.realm.name, 'TestRealm')

class CharacterModelTestCase(TestCase):
    def setUp(self):
        attendanceSetup(self)

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
        character = Character.objects.get(name='TestCharacterMain1')
        self.assertEqual(str(character), 'TestCharacterMain1')

    def test_get_characters_alts(self):
        """Test that an Alt Character's Main is returned"""
        character_main = Character.objects.get(name='TestCharacterMain1')
        character_alt = Character.objects.get(name='TestCharacterAlt1')
        
        alts = character_main.get_alts

        for alt in alts:
            self.assertEqual(alt.main_character.name, 'TestCharacterMain1')
        
        self.assertEqual(character_alt.main_character.name, 'TestCharacterMain1')
        
    def test_get_raids_attended_count(self):
        """Test that the raid attendance counts are expected"""
        character_main = Character.objects.get(name='TestCharacterMain1')
        character_alt_non_required_raid = Character.objects.get(name='TestCharacterAlt1')
        character_alt_required_raid = Character.objects.get(name='TestCharacterAlt2')

        raids_attended_count_main = character_main.get_raids_attended_count
        raids_attended_count_alt_non_required = character_alt_non_required_raid.get_raids_attended_count
        raids_attended_count_alt_required = character_alt_required_raid.get_raids_attended_count

        self.assertEqual(raids_attended_count_main, 3)
        self.assertEqual(raids_attended_count_alt_non_required, 0)
        self.assertEqual(raids_attended_count_alt_required, 1)
        
    def test_get_eligible_raids_count(self):
        """Test that the eligible raid counts are expected"""
        character_main = Character.objects.get(name='TestCharacterMain1')
        character_main_overrides = Character.objects.get(name='TestCharacterMain2')
        character_main_overrides_surplus = Character.objects.get(name='TestCharacterMain3')
        
        character_alt_non_required_raid = Character.objects.get(name='TestCharacterAlt1')
        character_alt_required_raid = Character.objects.get(name='TestCharacterAlt2')
        character_alt_no_attendance = Character.objects.get(name='TestCharacterAlt3')

        raids_eligible_count_main = character_main.get_eligible_raids_count
        raids_eligible_count_main_overrides = character_main_overrides.get_eligible_raids_count
        raids_eligible_count_main_overrides_surplus = character_main_overrides_surplus.get_eligible_raids_count

        raids_eligible_count_alt_non_required = character_alt_non_required_raid.get_eligible_raids_count
        raids_eligible_count_alt_required = character_alt_required_raid.get_eligible_raids_count
        raids_eligible_count_alt_no_attendance = character_alt_no_attendance.get_eligible_raids_count

        self.assertEqual(raids_eligible_count_main, 1)
        self.assertEqual(raids_eligible_count_main_overrides, 4)
        self.assertEqual(raids_eligible_count_main_overrides_surplus, 5)
        
        self.assertEqual(raids_eligible_count_alt_non_required, 0)
        self.assertEqual(raids_eligible_count_alt_required, 0)
        self.assertEqual(raids_eligible_count_alt_no_attendance, 0)

    def test_get_attended_raids_percentage(self):
        """Test that the raid attendance percentages are expected"""
        character_main = Character.objects.get(name='TestCharacterMain1')
        character_main_overrides = Character.objects.get(name='TestCharacterMain2')
        character_main_overrides_surplus = Character.objects.get(name='TestCharacterMain3')
        
        character_alt_non_required_raid = Character.objects.get(name='TestCharacterAlt1')
        character_alt_required_raid = Character.objects.get(name='TestCharacterAlt2')
        character_alt_no_attendance = Character.objects.get(name='TestCharacterAlt3')

        raids_attended_percentage_main = character_main.get_attended_raids_percentage
        raids_attended_percentage_main_overrides = character_main_overrides.get_attended_raids_percentage
        raids_attended_percentage_main_overrides_surplus = character_main_overrides_surplus.get_attended_raids_percentage

        raids_attended_percentage_alt_non_required = character_alt_non_required_raid.get_attended_raids_percentage
        raids_attended_percentage_alt_required = character_alt_required_raid.get_attended_raids_percentage
        raids_attended_percentage_no_attendance = character_alt_no_attendance.get_attended_raids_percentage

        self.assertEqual(raids_attended_percentage_main, "100%")
        self.assertEqual(raids_attended_percentage_main_overrides, "100%")
        self.assertEqual(raids_attended_percentage_main_overrides_surplus, "80%")

        self.assertEqual(raids_attended_percentage_alt_non_required, '-')
        self.assertEqual(raids_attended_percentage_alt_required, '-')
        self.assertEqual(raids_attended_percentage_no_attendance, '-')

class InstanceModelTestCase(TestCase):
    def setUp(self):
        instanceSetup(self)
    def test_instance_name_is_returned(self):
        """The expected instance name is returned"""
        instance = Instance.objects.get(name='TestInstance1')
        self.assertEqual(str(instance), 'TestInstance1')

class NpcModelTestCase(TestCase):
    def setUp(self):
        npcSetup(self)
    def test_instance_name_is_returned(self):
        """The expected NPC name is returned"""
        npc = Npc.objects.get(name='TestNpc')
        self.assertEqual(str(npc), 'TestNpc')

class RaidModelTestCase(TestCase):
    def setUp(self):
        raidSetup(self)
    def test_raid_name_is_returned(self):
        """The expected Raid name is returned"""
        raid = Raid.objects.get(instance__name='TestInstance1')
        self.assertEqual(str(raid), 'January 01, 2020 - TestInstance1')

class LootModelTestCase(TestCase):
    def setUp(self):
        lootSetup(self)

    def test_item_name_is_returned(self):
        """The expected item name is returned from the Loot and Item models"""
        loot = Loot.objects.get(item__name='TestItem1')
        item = Item.objects.get(name='TestItem1')

        self.assertEqual(str(loot), 'TestItem1')
        self.assertEqual(str(item), 'TestItem1')
        self.assertEqual(loot.item.name, 'TestItem1')

class AttendanceModelTestCase(TestCase):
    def setUp(self):
        attendanceSetup(self)
    
    def test_attendance_name_is_returned(self):
        """The expected attendance name is returned"""
        attendance = Attendance.objects.get(raid__instance__name='TestInstance1')
        self.assertEqual(str(attendance), '2020-01-01 - TestInstance1: TestCharacterMain1')
        
class CharacterAdminTestCase(TestCase):
    def setUp(self):
        attendanceSetup(self)

    def test_alt_markup(self):
        """Test that the Character name is marked up for alts"""
        character_admin = CharacterAdmin(model=Character, admin_site=AdminSite())
        character_main = Character.objects.get(name='TestCharacterMain1')
        character_alt = Character.objects.get(name='TestCharacterAlt1')

        main_markup = character_admin.name_alt(character_main)
        alt_markup = character_admin.name_alt(character_alt)

        self.assertEqual(main_markup, 'TestCharacterMain1')
        self.assertEqual(alt_markup, 'TestCharacterAlt1*')

class LootAdminTestCase(TestCase):
    def setUp(self):
        lootSetup(self)

    def test_exceptional_markup(self):
        """Test that the Exceptional checkmark is only displayed when true"""
        loot_admin = LootAdmin(model=Loot, admin_site=AdminSite())
        loot_exceptional = Loot.objects.get(item__name='TestItem1')
        loot_standard = Loot.objects.get(item__name='TestItem2')

        checkmark_dislayed = loot_admin.exceptional_checkmark_only(loot_exceptional)
        checkmark_hidden = loot_admin.exceptional_checkmark_only(loot_standard)

        self.assertIsNotNone(checkmark_dislayed)
        self.assertEquals(checkmark_hidden, '')

    def test_has_tooltip(self):
        """Test that the Tooltip is only displayed when an item id is provided"""
        loot_admin = LootAdmin(model=Loot, admin_site=AdminSite())
        loot_without_tooltip = Loot.objects.get(item__name='TestItem1')
        loot_with_tooltip = Loot.objects.get(item__name='TestItem2')

        tooltip_dislayed = loot_admin.item_link(loot_with_tooltip)
        tooltip_hidden = loot_admin.item_link(loot_without_tooltip)
        self.assertRegex(tooltip_dislayed, r'.*https://.*')
        self.assertEquals(tooltip_hidden, loot_without_tooltip.item.name)

class ItemAdminTestCase(TestCase):
    def setUp(self):
        lootSetup(self)

    def test_has_tooltip(self):
        """Test that the Tooltip is only displayed when an item id is provided"""
        item_admin = ItemAdmin(model=Item, admin_site=AdminSite())
        item_without_tooltip = Item.objects.get(name='TestItem1')
        item_with_tooltip = Item.objects.get(name='TestItem2')

        tooltip_dislayed = item_admin.item_link(item_with_tooltip)
        tooltip_hidden = item_admin.item_link(item_without_tooltip)
        self.assertRegex(tooltip_dislayed, r'.*href=.*')
        self.assertEquals(tooltip_hidden, item_without_tooltip.name)