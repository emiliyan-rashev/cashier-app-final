from django.contrib.auth import get_user_model
from django.db import models
from cashier.households.models import HouseholdProfile
from cashier.mixins.validators import validate_integer

UserModel = get_user_model()


class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, validators=[validate_integer])
    apartment = models.IntegerField(null=True, blank=True)
    # household on_delete to be tested after household tests are added
    household = models.ForeignKey(
        HouseholdProfile(apartment=apartment),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    live_in_apartment = models.BooleanField(default=True)
    newsletter_agreement = models.BooleanField(default=False)
    is_household_admin = models.BooleanField(default=False)
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )
