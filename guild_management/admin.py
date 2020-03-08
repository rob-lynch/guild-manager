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

class ActiveFilter(SimpleListFilter):
    title = 'membership status'
    parameter_name = 'membership'

    def lookups(self, request, model_admin):

        return (
            (None,('Active')),
            ('inactive',('Inactive')),
            ('all',('All')),
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }


    def queryset(self, request, queryset):
        model_name = queryset.model.__name__

        def define_filter(self, model_name,filter_value):
            if model_name == 'Character':
                return queryset.filter(active=filter_value)
            if model_name == 'Attendance':
                return queryset.filter(raid_character__active=filter_value)
            if model_name == 'Loot':
                return queryset.filter(character__active=filter_value)
            
        
        if self.value() in ('active', None):
            return define_filter(self, model_name, True)
        elif self.value() == 'inactive':
            return define_filter(self, model_name, False)
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
        ActiveFilter,
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
        ActiveFilter,
        AltFilter,
        'raid',
        'raid_character',
        'raid__instance__name',
        'raid__instance_date',
    )
    
    search_fields = ( 
        'raid_character__name', 
        'raid__instance__name',
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
        ActiveFilter,
        AltFilter,
        'raid',
        'boss',
        'character',
        'priority',
        'exceptional',
    )

    search_fields = (
        'raid__instance__name',
        'character__name',
        'boss__name',
        'item__name',
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

    search_fields = (
        'name',
        'item_id',
    )

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