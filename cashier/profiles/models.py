from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from cashier.households.models import HouseholdProfile


def validate_integer(value):
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
    phone_number = models.CharField(max_length=10,validators=[validate_integer])
    apartment = models.IntegerField() #TODO: add confirmation logic - If the household exists: send email to notify the hh admin and show a confirmation view to hh admin. Else: Do the same, but to the main admin. If there isn't an admin, block the registration
    household = models.ForeignKey(HouseholdProfile(apartment=apartment), on_delete=models.CASCADE, null=True, blank=True) #TODO: This should be created by an Admin when the user is approved for the household
    live_in_apartment = models.BooleanField(default=True)
    newsletter_agreement = models.BooleanField(default=False)
    is_household_admin = models.BooleanField(default=False)
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )


