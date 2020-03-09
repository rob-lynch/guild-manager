from django.test import TestCase
from guild_management.models import Realm

# Create your tests here.


class RealmTestCase(TestCase):
    def setUp(self):
        Realm.objects.create(name="TestRealm")

    def test_realm_is_created(self):
        """The Realm that is created returns the expected name"""
        realm = Realm.objects.get(name="TestRealm")
        self.assertEqual(realm.name, 'TestRealm')