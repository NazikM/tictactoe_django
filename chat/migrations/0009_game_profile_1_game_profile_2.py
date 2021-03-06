# Generated by Django 4.0.5 on 2022-07-06 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='profile_1',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='first', to='chat.player'),
        ),
        migrations.AddField(
            model_name='game',
            name='profile_2',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='second', to='chat.player'),
        ),
    ]
