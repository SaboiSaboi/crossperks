# Generated by Django 5.1.3 on 2025-03-13 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0012_remove_businessprofile_qr_code_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="businessprofile",
            name="onboarded",
            field=models.BooleanField(default=False),
        ),
    ]
