# Generated by Django 5.0.6 on 2024-05-30 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("vtso", "0006_rename_harbourlog_visit_alter_visit_table"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="company",
            options={"verbose_name_plural": "Companies"},
        ),
    ]
