# Generated by Django 4.2 on 2023-04-18 13:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="first_name",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="customer",
            name="last_name",
            field=models.CharField(max_length=100, null=True),
        ),
    ]