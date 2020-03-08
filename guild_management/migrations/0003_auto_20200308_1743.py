# Generated by Django 3.0.3 on 2020-03-08 22:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guild_management', '0002_character_main_character'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='character',
            options={'ordering': ['-main_character__name', 'name']},
        ),
        migrations.AlterField(
            model_name='attendance',
            name='raid_character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guild_management.Character', verbose_name='character'),
        ),
        migrations.AlterField(
            model_name='character',
            name='playable_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='guild_management.PlayableClass', verbose_name='class'),
        ),
        migrations.AlterField(
            model_name='instance',
            name='name',
            field=models.CharField(max_length=64, unique=True, verbose_name='instance name'),
        ),
    ]
