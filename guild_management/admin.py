from django.contrib import admin
from .models import *
from .resources import *
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

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
        'realm',
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
    list_display = (
        'raid',
        'character',
        'item',
    )

    list_filter = (
        'raid',
        'item',
        'character',
    )
    
    resource_class = AttendanceResource

admin.site.register(PlayableClass)
admin.site.register(Race)
admin.site.register(Rank)
admin.site.register(Realm)
admin.site.register(Instance)
admin.site.register(Item)
admin.site.register(Guild)
admin.site.register(Raid)
admin.site.register(Loot, LootAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Attendance, AttendanceAdmin)