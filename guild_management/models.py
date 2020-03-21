from django.contrib.admin.models import LogEntry
from django.conf import settings
from django.db import models
from django.db.models import Max
from django.core.cache import cache
import datetime
from datetime import timedelta, timezone

def get_set_cache(self, key_name, data=None):
    if hasattr(self, 'id'):
        cache_key = key_name + '_' + str(self.id)
    else:
        cache_key = key_name

    if data and self.cache_ttl > 0:
        #print('Setting cache. Key:' + cache_key + ' Value: ' + str(data))
        cache.set(cache_key, data)
    else:
        now = datetime.datetime.now(timezone.utc)
        last_updated = LogEntry.objects.filter(content_type_id__app_label='guild_management').aggregate(Max('action_time'))
        cache_ttl = cache.ttl(cache_key)
        cache_ttl_date = now + timedelta(seconds=cache_ttl)
        cache_timeout = settings.CACHES['default']['TIMEOUT']
        cache_ttl_delta =  cache_timeout - cache_ttl
        cache_set_date = now - timedelta(seconds=cache_ttl_delta)

 #       print('')
 #       print('----------------------------------')
 #       print('')
 #       print('Last Updated: ' + str(last_updated['action_time__max']))
#        print('Cache Timeout: ' + str(cache_timeout))
#        print('Cache TTL: ' + str(cache_ttl))
#        print('Cache TTL Delta: ' + str(cache_ttl_delta))
#        print('Cache Expire Set Date: ' + str(cache_set_date))
#        print('Cache Expiry Date: ' + str(cache_ttl_date))

        if last_updated['action_time__max'] < cache_set_date  :
            cache_data = cache.get(cache_key)
            if cache_data:
                #print('++++Getting cache. Key:' + cache_key + ' Value: ' + str(cache_data))
                get_set_cache(self, cache_key, cache_data)
            return cache_data
        #else:
            #print('++++Cache too old. Key:' + cache_key)

class PlayableClass(models.Model):
    def __str__(self):
       return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
    
    name = models.CharField('Class', max_length=32, unique=True)

class Item(models.Model):
    def __str__(self):
       return self.name
    
    class Meta:
        ordering = ['name']

    name = models.CharField('Item name', max_length=64)
    item_id = models.SmallIntegerField(blank=True, null=True, unique=True)

class Race(models.Model):
    def __str__(self):
       return self.name

    class Meta:
        ordering = ['name']
    
    name = models.CharField('Race', max_length=32, unique=True)
   
class Rank(models.Model):
    def __str__(self):
       return self.name

    class Meta:
        ordering = ['name']
    
    name = models.CharField('Rank', max_length=32, unique=True)
   
class Realm(models.Model):
    def __str__(self):
       return self.name

    class Meta:
        ordering = ['name']
    
    name = models.CharField('Realm', max_length=32, unique=True)
   
class Instance(models.Model):
    def __str__(self):
       return self.name

    class Meta:
        ordering = ['name']
    
    name = models.CharField('instance name', max_length=64, unique=True)
    dkp = models.SmallIntegerField(blank=False)
   
class Guild(models.Model):
    def __str__(self):
       return self.name

    class Meta:
        ordering = ['name']
    
    name = models.CharField('Guild name', max_length=32, unique=True)
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE)

class Raid(models.Model):
    def __str__(self):
       return self.unique_instance_name
    
    class Meta:
        ordering = ['-instance_date','instance__name']

    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    instance_date = models.DateField()
    required = models.BooleanField(default=True)
    
    @property
    def get_unique_instance(self):
        key_name = 'instance'
        data = get_set_cache(self, key_name)

        if not data:
            data = self.instance_date.strftime('%B %d, %Y') + ' - ' + self.instance.name
        
        return data

    unique_instance_name = get_unique_instance

class Character(models.Model):
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-main_character__name','name',]

    name = models.CharField('Character name', max_length=32, unique=True)
    level = models.SmallIntegerField(blank=False, default=60)
    guild_join_date = models.DateField(null=True, blank=True)
    raid_eligibility_date = models.DateField(null=True, blank=True)
    playable_class = models.ForeignKey(PlayableClass, on_delete=models.CASCADE, verbose_name='class', null=True, blank=True)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, null=True, blank=True)
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE, default=1)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, default=4)
    eligible_raids_override = models.SmallIntegerField(blank=False, default=0)
    attended_raids_override = models.SmallIntegerField(blank=False, default=0)
    main_character = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=True)
    
    @property
    def get_alts(self):
        key_name = 'character_alts'
        data = get_set_cache(self, key_name)

        if not data:
            data = Character.objects.filter(main_character=self.id)
        
        return data
        
    alts = get_alts

    @property
    def get_raids_attended_count(self):
        alt_attended_actual = 0
        alt_raid_ids = []

        if self.alts:
            for alt in self.alts:
                key_name = 'alt_attendance_count'
                data = get_set_cache(self, key_name)

                if not data:   
                    data = Attendance.objects.filter(raid__required=True).filter(raid_character__id=alt.id).distinct('raid__instance_date')

                alt_attended = data
                alt_attended_actual += alt_attended.count()

                for raids in alt_attended:
                    alt_raid_ids.append(raids.id)
                
                if alt_attended_actual > 0:
                    break
        
        cache_key = 'attendance_actual_' + str(self.id)
        data = cache.get(cache_key)
        if not data:   
            data = Attendance.objects.filter(raid__required=True).filter(raid_character__id=self.id).exclude(raid_id__in=alt_raid_ids).distinct('raid__instance_date').count()
        cache.set(cache_key, data)

        attended_actual = data

        attended_adjusted =  attended_actual + self.attended_raids_override + alt_attended_actual

        return attended_adjusted

    @property
    def get_eligible_raids_count(self):
        if self.raid_eligibility_date:
            eligibility_date = self.raid_eligibility_date.strftime('%Y-%m-%d')
            cache_key = 'eligible_actual_' + str(self.id)
            data = cache.get(cache_key)
            if not data:   
                data = Raid.objects.filter(required=True).filter(instance_date__gte=eligibility_date).distinct('instance_date').count()
            cache.set(cache_key, data)
            
            eligible_actual = data
            eligible_adjusted = eligible_actual + self.eligible_raids_override
            return eligible_adjusted
        else:
            return 0

    number_or_raids_attended = get_raids_attended_count
    number_of_eligible_raids = get_eligible_raids_count
    
    @property
    def get_attended_raids_percentage(self):
        if self.number_of_eligible_raids:
            if self.number_or_raids_attended > self.number_of_eligible_raids:
                attended = self.number_of_eligible_raids
            else: 
                attended = self.number_or_raids_attended
            return str(int((attended / self.number_of_eligible_raids) * 100)) + '%'
        else: 
            return "-"

    attendance_percentage = get_attended_raids_percentage

class Npc(models.Model):
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['instance_appearance_order','name',]

    name = models.CharField('NPC name', max_length=32, unique=True)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE, null=True)
    instance_appearance_order = models.SmallIntegerField(blank=True, null=True)

class Loot(models.Model):
    def __str__(self):
        return self.item.name
    
    class Meta:
        ordering = ['-raid__instance_date','raid__instance__name','boss__instance_appearance_order','character__name','item__name']
        verbose_name_plural = 'loot'

    character = models.ForeignKey(Character, on_delete=models.CASCADE, blank=True, null=True)
    raid = models.ForeignKey(Raid, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    boss = models.ForeignKey(Npc, on_delete=models.CASCADE, null=True, blank=True)
    priority = models.BooleanField()
    exceptional = models.BooleanField()
    notes = models.TextField(blank=True, null=True)

class Attendance(models.Model):    
    def __str__(self):
        return str(self.raid.instance_date) + ' - ' + self.raid.instance.name + ': ' + self.raid_character.name

    class Meta:
        ordering = ['-raid__instance_date','raid_character__name']
        verbose_name_plural = 'attendance'
    
    raid_character = models.ForeignKey(Character, on_delete=models.CASCADE, verbose_name='character')
    raid = models.ForeignKey(Raid, on_delete=models.CASCADE)