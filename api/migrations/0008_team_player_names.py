# Generated by Django 4.1.3 on 2022-11-30 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_team_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='player_names',
            field=models.TextField(default='none'),
        ),
    ]
