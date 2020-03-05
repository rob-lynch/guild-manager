from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from .models import *

class CharacterResource(resources.ModelResource):
    guild = fields.Field(
        column_name='guild',
        attribute='guild',
        widget=ForeignKeyWidget(Guild, 'name')
    )

    playable_class = fields.Field(
        column_name='playable_class',
        attribute='playable_class',
        widget=ForeignKeyWidget(PlayableClass, 'name')
    )

    race = fields.Field(
        column_name='race',
        attribute='race',
        widget=ForeignKeyWidget(Race, 'name')
    )

    rank = fields.Field(
        column_name='rank',
        attribute='rank',
        widget=ForeignKeyWidget(Rank, 'name')
    )

    realm = fields.Field(
        column_name='realm',
        attribute='realm',
        widget=ForeignKeyWidget(Realm, 'name')
    )

    class Meta:
        model = Character

class AttendanceResource(resources.ModelResource):
    raid = fields.Field(
        column_name='raid',
        attribute='raid',
        widget=ForeignKeyWidget(Raid, 'instance_date')
    )

    raid_character = fields.Field(
        column_name='raid_character',
        attribute='raid_character',
        widget=ForeignKeyWidget(Character, 'name')
    )

    class Meta:
        model = Attendance

class LootResource(resources.ModelResource):
    character = fields.Field(
        column_name='character',
        attribute='character',
        widget=ForeignKeyWidget(Character, 'name')
    )

    raid = fields.Field(
        column_name='raid',
        attribute='raid',
        widget=ForeignKeyWidget(Raid, 'instance_date')
    )

    item = fields.Field(
        column_name='item',
        attribute='item',
        widget=ForeignKeyWidget(Character, 'name')
    )

    class Meta:
        model = Loot