# Generated by Django 5.0.6 on 2024-05-27 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("vtso", "0005_alter_ship_year_built_harbourlog"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="HarbourLog",
            new_name="Visit",
        ),
        migrations.AlterModelTable(
            name="visit",
            table="VISIT",
        ),
    ]
