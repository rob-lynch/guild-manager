# Generated by Django 3.0.3 on 2020-03-07 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guild_management', '0002_npc_instance_appearance_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loot',
            options={'ordering': ['-raid__instance_date', 'boss__name', 'boss__instance_appearance_order', 'character__name', 'item__name'], 'verbose_name_plural': 'loot'},
        ),
    ]
