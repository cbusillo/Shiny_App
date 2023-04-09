# Generated by Django 4.2 on 2023-04-09 13:14

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ls_customer_id", models.IntegerField(null=True)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("title", models.CharField(blank=True, max_length=10, null=True)),
                ("company", models.CharField(blank=True, max_length=100, null=True)),
                ("create_time", models.DateTimeField(auto_now_add=True)),
                ("update_time", models.DateTimeField(auto_now=True)),
                ("updated_from_ls_time", models.DateTimeField(null=True)),
                ("archived", models.BooleanField()),
                ("contact_id", models.IntegerField()),
                ("credit_account_id", models.IntegerField(blank=True, null=True)),
                ("customer_type_id", models.IntegerField()),
                ("discount_id", models.IntegerField(blank=True, null=True)),
                ("tax_category_id", models.IntegerField(blank=True, null=True)),
                ("is_modified", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Phone",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, region=None
                    ),
                ),
                ("use_type", models.CharField(max_length=20)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="phones",
                        to="customers.customer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Email",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("address", models.EmailField(max_length=254)),
                ("use_type", models.CharField(max_length=100)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="emails",
                        to="customers.customer",
                    ),
                ),
            ],
        ),
    ]
