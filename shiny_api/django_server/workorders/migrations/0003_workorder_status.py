# Generated by Django 4.2 on 2023-04-11 16:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("workorders", "0002_workorder_update_from_ls_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="workorder",
            name="status",
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
