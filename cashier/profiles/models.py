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
    apartment = models.IntegerField() #Using 0 as a feault value when a superuser is created or when a user is reject. Not the best approach. Maybe this field should be optional at some point. When it is optional and user logs in, they should be directly redirected to their profile and shouldn't have permissions for anything else
    household = models.ForeignKey(HouseholdProfile(apartment=apartment), on_delete=models.SET_NULL, null=True, blank=True)
    live_in_apartment = models.BooleanField(default=True)
    newsletter_agreement = models.BooleanField(default=False)
    is_household_admin = models.BooleanField(default=False)
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )


