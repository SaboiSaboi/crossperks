# Generated by Django 5.1.3 on 2025-03-08 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "account",
            "0009_remove_perk_assigned_to_remove_perk_expiration_date_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="perk",
            name="title",
            field=models.CharField(max_length=255),
        ),
    ]
