from django.db.models.signals import post_save
from django.dispatch import receiver

from cashier.payments.models import IndividualPayment, PaymentsAdmin
from cashier.profiles.models import UserProfile
from cashier.users.models import cashierUser


@receiver(post_save, sender=UserProfile)
def profile_updated(instance, **kwargs):
    payment_profile = IndividualPayment(pk=instance.user_id)
    payment_profile.save()

@receiver(post_save, sender=cashierUser)
def super_user_created(instance, created, **kwargs):
    if created and not PaymentsAdmin.objects.exists():
        if cashierUser.objects.get(id=instance.id).is_superuser:
            admin_payment_profile = PaymentsAdmin(pk=instance.id)
            admin_payment_profile.save()

