# Generated by Django 4.1.3 on 2023-02-04 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_contact_is_resolved'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
    ]