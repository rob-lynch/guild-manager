from django.contrib import admin
from .models import *
from .resources import *
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from django.utils.html import mark_safe
from django.contrib.admin import SimpleListFilter

class AltFilter(SimpleListFilter):
    title = 'character type'
    parameter_name = 'character_type'

    def lookups(self, request, model_admin):

        return (
            ('alt',('Alt')),
            ('main',('Main')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'alt':
            return queryset.exclude(main_character=None)
        elif self.value() == 'main':
            return queryset.filter(main_character=None)
        else:
            return queryset

class CharacterAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    class Media:
        js = ('guild_management/js/list_filter_collapse.js',)
        
    list_display = (
        'name_alt',
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
        AltFilter,
        'level', 
        'guild_join_date',
        'raid_eligibility_date',
        'playable_class',
        'race',
        'guild',
        'rank',
    )

    search_fields = ('name',)

    def name_alt(self,obj):
        if obj.main_character:
            return obj.name + '*'
        else:
            return obj.name

    name_alt.allow_tags = True
    name_alt.short_description = "Character Name"

    resource_class = CharacterResource

class AttendanceAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    class Media:
        js = ('guild_management/js/list_filter_collapse.js',)
    
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
        js = ('guild_management/js/list_filter_collapse.js','https://classicdb.ch/templates/wowhead/js/power.js',)

    list_display = (
        'raid',
        'boss',
        'character',
        'item_link',
        'priority',
        'exceptional_checkmark_only',
        'notes',
    )

    list_filter = (
        'raid',
        'boss',
        'character',
        'priority',
        'exceptional',
    )

    def item_link(self,obj):
        if obj.item.item_id:
            return mark_safe('<a href="https://classicdb.ch/?item=%s" target="blank" rel="item=%s">%s</a>' % (obj.item.item_id, obj.item.item_id, obj.item))
        else:
            return obj.item.name

    item_link.allow_tags = True
    item_link.short_description = "Item"
    
    def exceptional_checkmark_only(self,obj):
        if obj.exceptional == True:
            return mark_safe('<img src="/static/admin/img/icon-yes.svg" alt="True">')
        else:
            return ""

    exceptional_checkmark_only.allow_tags = True
    exceptional_checkmark_only.short_description = "Exceptional"
    
    resource_class = AttendanceResource

class ItemAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    class Media:
        js = ('https://classicdb.ch/templates/wowhead/js/power.js',)

    list_display = (
        'item_link',
        'item_id',
    )

    search_fields = ('name','item_id',)

    def item_link(self,obj):
        if obj.item_id:
            return mark_safe('<a href="%s/change/" rel="item=%s">%s</a>' % (obj.id, obj.item_id, obj.name))
        else:
            return obj.name

    item_link.allow_tags = True
    item_link.short_description = "Item"

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