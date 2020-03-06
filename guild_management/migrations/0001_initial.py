# Generated by Django 3.0.3 on 2020-03-06 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Character name')),
                ('level', models.SmallIntegerField(default=60)),
                ('guild_join_date', models.DateField(blank=True, null=True)),
                ('raid_eligibility_date', models.DateField(blank=True, null=True)),
                ('raid_count_override', models.SmallIntegerField(default=0)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Instance name')),
                ('dkp', models.SmallIntegerField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Item name')),
                ('item_id', models.SmallIntegerField(blank=True, null=True, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PlayableClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Class')),
            ],
            options={
                'verbose_name': 'Class',
                'verbose_name_plural': 'Classes',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Race')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Rank')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Realm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Realm')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Raid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance_date', models.DateField()),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guild_management.Instance')),
            ],
            options={
                'ordering': ['-instance_date', 'instance__name'],
            },
        ),
        migrations.CreateModel(
            name='Npc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='NPC name')),
                ('instance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='guild_management.Instance')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Loot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.BooleanField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('boss', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guild_management.Npc')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guild_management.Character')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guild_management.Item')),
                ('raid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guild_management.Raid')),
            ],
            options={
                'verbose_name_plural': 'loot',
                'ordering': ['-raid__instance_date', 'character__name', 'item__name'],
            },
        ),
        migrations.CreateModel(
            name='Guild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Guild name')),
                ('realm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guild_management.Realm')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='character',
            name='guild',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='guild_management.Guild'),
        ),
        migrations.AddField(
            model_name='character',
            name='playable_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='guild_management.PlayableClass', verbose_name='Class'),
        ),
        migrations.AddField(
            model_name='character',
            name='race',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='guild_management.Race'),
        ),
        migrations.AddField(
            model_name='character',
            name='rank',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='guild_management.Rank'),
        ),
        migrations.AddField(
            model_name='character',
            name='realm',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='guild_management.Realm'),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guild_management.Raid')),
                ('raid_character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guild_management.Character', verbose_name='Character')),
            ],
            options={
                'verbose_name_plural': 'attendance',
                'ordering': ['-raid__instance_date', 'raid_character__name'],
            },
        ),
    ]
