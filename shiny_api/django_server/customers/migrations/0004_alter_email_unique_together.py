# Generated by Django 4.2 on 2023-04-10 14:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0003_alter_phone_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="email",
            unique_together={("address", "customer", "use_type")},
        ),
    ]