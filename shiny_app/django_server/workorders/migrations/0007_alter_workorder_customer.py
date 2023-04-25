# Generated by Django 4.2 on 2023-04-25 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0004_alter_customer_ls_customer_id"),
        ("workorders", "0006_alter_workorder_customer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="workorder",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="workorders_related",
                to="customers.customer",
            ),
        ),
    ]
