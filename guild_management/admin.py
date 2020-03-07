from django.contrib import admin
from .models import *
from .resources import *
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from django.utils.html import mark_safe

class CharacterAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = (
        'name', 
        'level', 
        'guild_join_date',
        'raid_eligibility_date',
        'playable_class',
        'race',
        'rank',
        'number_of_eligible_raids',
        'number_or_raids_attended',
        'attendance_percentage',
    )

    list_filter = (
        'level', 
        'guild_join_date',
        'raid_eligibility_date',
        'playable_class',
        'race',
        'guild',
        'rank',
    )

    resource_class = CharacterResource

class AttendanceAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = (
        'raid',
        'raid_character',
    )

    list_filter = (
        'raid',
        'raid_character',
    )
    
    resource_class = AttendanceResource

class LootAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    class Media:
        js = ("https://classicdb.ch/templates/wowhead/js/power.js",)

    list_display = (
        'raid',
        'boss',
        'character',
        'item_link',
        'priority',
        'notes',
    )

    list_filter = (
        'raid',
        'character',
        'priority',
    )

    def item_link(self,obj):
        if obj.item.item_id:
            return mark_safe('<a href="https://classicdb.ch/?item=%s" target="blank" rel="item=%s">%s</a>' % (obj.item.item_id, obj.item.item_id, obj.item))
        else:
            return obj.item.name
    item_link.allow_tags = True
    item_link.short_description = "Item"
    
    resource_class = AttendanceResource

class ItemAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    class Media:
        js = ("https://classicdb.ch/templates/wowhead/js/power.js",)

    list_display = (
        'item_link',
        'item_id',
    )

    def item_link(self,obj):
        if obj.item_id:
            return mark_safe('<a href="%s/change/" rel="item=%s">%s</a>' % (obj.id, obj.item_id, obj.name))
        else:
            return obj.name
    resource_class = ItemResource

admin.site.register(PlayableClass)
admin.site.register(Race)
admin.site.register(Rank)
admin.site.register(Realm)
admin.site.register(Instance)
admin.site.register(Item, ItemAdmin)
admin.site.register(Guild)
admin.site.register(Npc)
admin.site.register(Raid)
admin.site.register(Loot, LootAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Attendance, AttendanceAdmin)