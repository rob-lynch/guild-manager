from django.contrib import admin
from .models import Attendance, Character, Loot, Raid, Npc, Item, Guild, PlayableClass, Instance, Realm, Rank, Race, get_set_cache
from .resources import CharacterResource, AttendanceResource, LootResource, ItemResource
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from django.utils.html import mark_safe
from django.contrib.admin import SimpleListFilter
from django.db.models import Q

class AltFilter(SimpleListFilter):
    title = 'character type'
    parameter_name = 'character_type'

    def lookups(self, request, model_admin):

        return (
            ('alt',('Alt')),
            ('main',('Main')),
        )

    def queryset(self, request, queryset):
        model_name = queryset.model.__name__

        def define_filter(model_name, filter_value):
            if model_name == 'Character':
                if filter_value:
                    return queryset.filter(main_character=None)
                else:
                    return queryset.exclude(main_character=None)
            if model_name == 'Attendance':
                if filter_value:
                    return queryset.filter(raid_character__main_character=None)
                else:
                    return queryset.exclude(raid_character__main_character=None)
            if model_name == 'Loot':
                if filter_value:
                    return queryset.filter(character__main_character=None)
                else:
                    return queryset.exclude(character__main_character=None)

        if self.value() == 'alt':
            return define_filter(model_name, False)
        elif self.value() == 'main':
            return define_filter(model_name, True)
        else:
            return queryset

class CharacterFilter(SimpleListFilter):
    title = 'character'
    parameter_name = 'character_list'

    def parse_character_list_to_int(self, character_list):
        id_list_string = character_list.split(',')
        return list(map(int, id_list_string))

    def define_membership(self, request):
        if 'membership' in request.GET:
            if request.GET['membership'] == 'active':
                return True
            else:
                return False
        else:
            return True
    
    def lookups(self, request, model_admin):
        key_name = 'character_lookup'
        data = get_set_cache(self, key_name)
        
        if not data:
            data = Character.objects.filter(active=CharacterFilter.define_membership(self, request))
        
        get_set_cache(self, key_name, data)

        characters = data
        incoming_ids = None

        if 'character_list' in request.GET:
            incoming_ids = request.GET['character_list'].split(',')

        character_tuple = ()
        for c in characters:
            if incoming_ids:
                unique_id_list = set([*incoming_ids, str(c.id)])
                full_id_list = ','.join(unique_id_list)
            else:
                full_id_list = str(c.id)
            character_tuple = (*character_tuple, (full_id_list,(c.name)))

        return character_tuple

    def queryset(self, request, queryset):
        if 'character_list' in request.GET:
            character_ids = CharacterFilter.parse_character_list_to_int(self, request.GET['character_list'])
            return queryset.filter(character__id__in=character_ids)
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

        def define_filter(model_name, filter_value):
            if model_name == 'Character':
                return queryset.filter(active=filter_value)
            if model_name == 'Attendance':
                return queryset.filter(raid_character__active=filter_value)
            if model_name == 'Loot':
                return queryset.filter(Q(character__active=filter_value) | Q(character__active=None))
        if self.value() in ('active', None):
            return define_filter(model_name, True)
        elif self.value() == 'inactive':
            return define_filter(model_name, False)
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
        CharacterFilter,
        'raid',
        'boss',
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
    
    resource_class = LootResource

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