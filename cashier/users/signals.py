from django.db.models.signals import post_save

from cashier.profiles.models import UserProfile
from cashier.users.models import cashierUser
from django.dispatch import receiver

@receiver(post_save, sender=cashierUser)
def super_user_created(instance, created, **kwargs):
    if created:
        if cashierUser.objects.get(id=instance.id).is_superuser:
            profile = UserProfile(first_name='', last_name='', email=instance.id, phone_number='', apartment=0,
                               user=cashierUser.objects.get(id=instance.id))
            profile.save()
