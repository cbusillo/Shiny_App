# Generated by Django 4.2 on 2023-04-20 03:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("serials", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="serial",
            name="serial_number",
            field=models.CharField(max_length=50, null=True),
        ),
    ]