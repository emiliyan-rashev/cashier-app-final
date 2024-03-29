# Generated by Django 4.2.6 on 2023-10-05 22:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mixins.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0002_alter_contactdetails_phone"),
        ("households", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "phone_number",
                    models.CharField(
                        max_length=10, validators=[mixins.validators.validate_integer]
                    ),
                ),
                ("apartment", models.IntegerField(blank=True, null=True)),
                ("live_in_apartment", models.BooleanField(default=True)),
                ("newsletter_agreement", models.BooleanField(default=False)),
                ("is_household_admin", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "household",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="households.householdprofile",
                    ),
                ),
            ],
        ),
    ]
