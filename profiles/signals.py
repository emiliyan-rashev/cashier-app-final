from django.db.models.signals import post_save
from django.dispatch import receiver
from profiles.models import UserProfile


# To be tested after the household profile signals are tested
@receiver(post_save, sender=UserProfile)
def apartment_changed(instance, **kwargs):
    form = UserProfile.objects.get(user=instance.user)
    if form.household and form.household.apartment != form.apartment:
        form.apartment = None
        form.household = None
        form.is_household_admin = False
        form.save()
    if not form.household and form.is_household_admin:
        form.apartment = None
        form.is_household_admin = False
        form.save()
