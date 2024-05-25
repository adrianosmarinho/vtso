# Generated by Django 5.0.6 on 2024-05-25 08:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vtso", "0003_harbour_alter_person_email"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="harbour",
            table="HARBOUR",
        ),
        migrations.AlterModelTable(
            name="person",
            table="PERSON",
        ),
        migrations.CreateModel(
            name="Ship",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                ("tonnage", models.PositiveIntegerField(blank=True, null=True)),
                ("max_load_draft", models.PositiveIntegerField(blank=True, null=True)),
                ("dry_draft", models.PositiveIntegerField(blank=True, null=True)),
                ("flag", models.CharField(blank=True, max_length=256, null=True)),
                ("beam", models.PositiveIntegerField(blank=True, null=True)),
                ("length", models.PositiveIntegerField(blank=True, null=True)),
                ("year_built", models.CharField(blank=True, max_length=4, null=True)),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("bulk carrier", "Bulk Carrier"),
                            ("fishing", "Fishing"),
                            ("submarine", "Submarine"),
                            ("tanker", "Tanker"),
                            ("cruise ship", "Cruise Ship"),
                        ],
                        max_length=256,
                        null=True,
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="vtso.company"
                    ),
                ),
            ],
            options={
                "db_table": "SHIP",
            },
        ),
    ]
