from django.db.models.signals import post_save, pre_save, pre_init
from django.dispatch import receiver

from cashier.news.models import News
from cashier.payments.models import IndividualPayment, PaymentsAdmin, TaxesPerMonth, SalariesPerMonth, SalariesPayment, IndividualTaxesPayed, SalariesPayedPerMonth
from cashier.profiles.models import UserProfile
from cashier.users.models import cashierUser
import datetime

@receiver(post_save, sender=UserProfile)
def profile_updated(instance, **kwargs):
    if not IndividualPayment.objects.filter(pk=instance.user_id):
        payment_profile = IndividualPayment(pk=instance.user_id)
        payment_profile.save()
        tax_profile = IndividualTaxesPayed(pk=instance.user_id)
        tax_profile.save()

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

    if created and not SalariesPayment.objects.exists():
        if cashierUser.objects.get(id=instance.id).is_superuser:
            taxes_per_month = SalariesPayment(pk=1)
            taxes_per_month.save()

    if created and not SalariesPayedPerMonth.objects.exists():
        if cashierUser.objects.get(id=instance.id).is_superuser:
            taxes_per_month = SalariesPayedPerMonth(pk=1)
            taxes_per_month.save()

@receiver(post_save, sender=PaymentsAdmin)
def admin_payments_updated(**kwargs):
    month_keys = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    curr_tax = PaymentsAdmin.objects.first().individual_monthly_tax
    curr_salaries = PaymentsAdmin.objects.first().salaries
    curr_month = datetime.date.today().month
    TaxesPerMonth.objects.filter(pk=1).update(**{str(curr_month) : curr_tax for curr_month in month_keys[curr_month:len(month_keys)]})
    SalariesPerMonth.objects.filter(pk=1).update(**{str(curr_month) : curr_salaries for curr_month in month_keys[curr_month:len(month_keys)]})

@receiver(pre_save, sender=IndividualPayment)
def individual_taxes_payed(instance, **kwargs):
    if IndividualPayment.objects.filter(id=instance.id):
        month_keys = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        form = IndividualPayment.objects.get(id=instance.id)
        tax_object = TaxesPerMonth.objects.first()
        taxes_needed_per_month = {curr_field.name : curr_field.value_from_object(tax_object) for curr_field in tax_object._meta.get_fields() if curr_field.name in month_keys}
        months_payed = [curr_field.name for curr_field in form._meta.get_fields() if curr_field.name != 'id' and curr_field.value_from_object(instance) == True and curr_field.value_from_object(form) == False]
        IndividualTaxesPayed.objects.filter(pk=instance.id).update(**{str(curr_month) : taxes_needed_per_month[curr_month] for curr_month in months_payed})

@receiver(pre_init, sender=IndividualPayment)
def get_available_payments(**kwargs):
    if 'args' in kwargs and len(kwargs['args']) > 0:
        curr_id = kwargs['args'][0]
        month_keys = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        tax_object = TaxesPerMonth.objects.first()
        payed_object = IndividualTaxesPayed.objects.get(pk=curr_id)
        taxes_payed_per_month = {curr_field.name : curr_field.value_from_object(payed_object) for curr_field in payed_object._meta.get_fields() if curr_field.name in month_keys}
        taxes_needed_per_month = {curr_field.name : curr_field.value_from_object(tax_object) for curr_field in tax_object._meta.get_fields() if curr_field.name in month_keys}
        IndividualPayment.objects.filter(pk=curr_id).update(**{str(curr_month) : taxes_needed_per_month[curr_month] <= taxes_payed_per_month[curr_month] for curr_month in month_keys})

@receiver(pre_save, sender=SalariesPayment)
def salaries_payed(instance, **kwargs):
    if SalariesPayment.objects.exists():
        month_keys = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        form = SalariesPayment.objects.first()
        salaries_object = SalariesPerMonth.objects.first()
        salaries_needed_per_month = {curr_field.name : curr_field.value_from_object(salaries_object) for curr_field in salaries_object._meta.get_fields() if curr_field.name in month_keys}
        months_payed = [curr_field.name for curr_field in form._meta.get_fields() if curr_field.name != 'id' and curr_field.value_from_object(instance) == True and curr_field.value_from_object(form) == False]
        SalariesPayedPerMonth.objects.filter(pk=1).update(**{str(curr_month) : salaries_needed_per_month[curr_month] for curr_month in months_payed})

@receiver(pre_init, sender=SalariesPayment)
def get_available_salaries(**kwargs):
    if SalariesPayedPerMonth.objects.exists():
        month_keys = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        salaries_object = SalariesPerMonth.objects.first()
        payed_object = SalariesPayedPerMonth.objects.first()
        slaries_payed_per_month = {curr_field.name : curr_field.value_from_object(payed_object) for curr_field in payed_object._meta.get_fields() if curr_field.name in month_keys}
        salaries_needed_per_month = {curr_field.name : curr_field.value_from_object(salaries_object) for curr_field in salaries_object._meta.get_fields() if curr_field.name in month_keys}
        SalariesPayment.objects.filter(pk=1).update(**{str(curr_month) : salaries_needed_per_month[curr_month] <= slaries_payed_per_month[curr_month] for curr_month in month_keys})

@receiver(pre_save, sender=PaymentsAdmin)
def get_available_salaries(instance, **kwargs):
    if PaymentsAdmin.objects.exists():
        new_tax = instance.individual_monthly_tax
        previous_tax = PaymentsAdmin.objects.first().individual_monthly_tax
        previous_salary = PaymentsAdmin.objects.first().salaries
        new_salary = instance.salaries
        if new_tax != previous_tax:
            notification = News(title='Tax changed', content=f'The tax has changed from {previous_tax} to {new_tax}')
            notification.save()
        if new_salary != previous_salary:
            notification = News(title='Salaries changed', content=f'The salaries have changed from {previous_salary} to {new_salary}')
            notification.save()


