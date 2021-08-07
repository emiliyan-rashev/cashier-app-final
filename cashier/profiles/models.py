from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from cashier.households.models import HouseholdProfile


def validate_even(value):
    if not value.isdigit():
        raise ValidationError(
            _('%(value)s is not a number'),
            params={'value': value},
        )
UserModel = get_user_model()

class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10,validators=[validate_even])
    apartment = models.IntegerField()
    household = models.ForeignKey(HouseholdProfile(apartment=apartment), on_delete=models.CASCADE, null=True)
    live_in_apartment = models.BooleanField(default=True)
    newsletter_agreement = models.BooleanField(default=False)
    is_household_admin = models.BooleanField(default=False)
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

