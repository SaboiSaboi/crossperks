# Generated by Django 5.1.7 on 2025-04-04 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0004_passwordresetcode_updated_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="deleted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="customuser",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
    ]
