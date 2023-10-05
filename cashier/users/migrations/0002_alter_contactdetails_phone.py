# Generated by Django 3.2.5 on 2021-08-25 22:49

import cashier.mixins.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contactdetails",
            name="phone",
            field=models.CharField(
                max_length=10, validators=[cashier.mixins.validators.validate_integer]
            ),
        ),
    ]
