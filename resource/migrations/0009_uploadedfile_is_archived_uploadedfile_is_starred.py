# Generated by Django 5.1.4 on 2025-02-17 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0008_alter_folder_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='is_archived',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='is_starred',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
