from django.db import models

import datetime 

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
    
    name = models.CharField('Instance name', max_length=64, unique=True)
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

    @property
    def get_unique_instance(self):
        return self.instance_date.strftime('%B %d, %Y') + ' - ' + self.instance.name

    unique_instance_name = get_unique_instance

class Character(models.Model):
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name',]

    name = models.CharField('Character name', max_length=32, unique=True)
    level = models.SmallIntegerField(blank=False, default=60)
    guild_join_date = models.DateField(null=True, blank=True)
    raid_eligibility_date = models.DateField(null=True, blank=True)
    playable_class = models.ForeignKey(PlayableClass, on_delete=models.CASCADE, verbose_name='Class', null=True, blank=True)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, null=True, blank=True)
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE, default=1)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, default=4)
    raid_count_override = models.SmallIntegerField(blank=False, default=0)

    @property
    def get_total_raids_count(self):
        return Raid.objects.count()

    total_raids_count = get_total_raids_count

    @property
    def get_raids_attended_count(self):
        attended_actual = Attendance.objects.filter(raid_character__id=self.id).count()
        attended_adjusted =  attended_actual + self.raid_count_override
        return attended_adjusted

    @property
    def get_eligible_raids_count(self):
        if self.raid_eligibility_date:
            eligibility_date = self.raid_eligibility_date.strftime('%Y-%m-%d')
            eligible_actual = Raid.objects.filter(instance_date__gt=eligibility_date).count()
            #This is incorrect
            eligible_adjusted = eligible_actual + self.raid_count_override
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
        ordering = ['name',]

    name = models.CharField('NPC name', max_length=32, unique=True)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE, null=True)
    instance_appearance_order = models.SmallIntegerField(blank=True, null=True, unique=True)

class Loot(models.Model):
    def __str__(self):
        return self.item.name
    
    class Meta:
        ordering = ['-raid__instance_date','boss__instance_appearance_order','character__name','item__name']
        verbose_name_plural = 'loot'

    character = models.ForeignKey(Character, on_delete=models.CASCADE, blank=True, null=True)
    raid = models.ForeignKey(Raid, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    boss = models.ForeignKey(Npc, on_delete=models.CASCADE, null=True, blank=True)
    priority = models.BooleanField()
    notes = models.TextField(blank=True, null=True)

class Attendance(models.Model):    
    def __str__(self):
        return str(self.raid.instance_date) + ' - ' + self.raid.instance.name + ': ' + self.raid_character.name

    class Meta:
        ordering = ['-raid__instance_date','raid_character__name']
        verbose_name_plural = 'attendance'
    
    raid_character = models.ForeignKey(Character, on_delete=models.CASCADE, verbose_name='Character')
    raid = models.ForeignKey(Raid, on_delete=models.CASCADE)