from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime
from cashier.payments.models import IndividualPayment, PaymentsAdmin, TaxesPerMonth, SalariesPerMonth
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
            admin_payment_profile = PaymentsAdmin(pk=1)
            admin_payment_profile.save()

    if created and not TaxesPerMonth.objects.exists():
        if cashierUser.objects.get(id=instance.id).is_superuser:
            taxes_per_month = TaxesPerMonth(pk=1)
            taxes_per_month.save()

    if created and not SalariesPerMonth.objects.exists():
        if cashierUser.objects.get(id=instance.id).is_superuser:
            taxes_per_month = SalariesPerMonth(pk=1)
            taxes_per_month.save()

@receiver(post_save, sender=PaymentsAdmin)
def admin_payments_updated(**kwargs):
    month_keys = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    curr_tax = PaymentsAdmin.objects.first().individual_monthly_tax
    curr_salaries = PaymentsAdmin.objects.first().salaries
    curr_month = datetime.date.today().month
    TaxesPerMonth.objects.filter(pk=1).update(**{str(curr_month) : curr_tax for curr_month in month_keys[curr_month:len(month_keys)]})
    SalariesPerMonth.objects.filter(pk=1).update(**{str(curr_month) : curr_salaries for curr_month in month_keys[curr_month:len(month_keys)]})

