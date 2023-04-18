# Generated by Django 4.2 on 2023-04-18 03:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("items", "0003_remove_item_serials"),
        ("customers", "0004_remove_customer_serials_remove_customer_workorders"),
        ("serials", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="serial",
            name="customer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="serials_related",
                to="customers.customer",
            ),
        ),
        migrations.AlterField(
            model_name="serial",
            name="item",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="serials_related",
                to="items.item",
            ),
        ),
    ]
