# Generated by Django 5.1.4 on 2025-05-04 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0012_filesharing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadedfile',
            name='shared_with',
        ),
    ]
