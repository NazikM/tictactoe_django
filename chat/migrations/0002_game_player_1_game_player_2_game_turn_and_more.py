# Generated by Django 4.0.5 on 2022-06-23 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='player_1',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='game',
            name='player_2',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='game',
            name='turn',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='game',
            name='u_name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
