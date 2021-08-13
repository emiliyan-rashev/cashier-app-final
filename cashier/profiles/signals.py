from django.db.models.signals import post_save
from django.dispatch import receiver

from cashier.profiles.models import UserProfile
from cashier.users.models import cashierUser


@receiver(post_save, sender=cashierUser)
def profile_updated(instance, **kwargs):
    if not cashierUser.objects.get(pk=instance.id).is_active:
        user_profile = UserProfile.objects.get(pk=instance.id)
        user_profile.live_in_apartment = False
        user_profile.is_household_admin = False
        user_profile.save()

@receiver(post_save, sender=UserProfile)
def apartment_changed(instance, **kwargs):
    form = UserProfile.objects.get(user=instance.user)
    if form.household and form.household.apartment != form.apartment:
        form.household = None
        form.is_household_admin = False
        form.save()
    if not form.household and form.is_household_admin:
        form.is_household_admin = False
        form.save()

