from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class HouseholdProfile(models.Model):
    apartment = models.IntegerField(null=True)
    apartment_percent_ideal_parts = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    household_balance = models.FloatField(blank=True, null=True, default=0)