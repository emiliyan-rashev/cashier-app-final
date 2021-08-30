from django.test import Client

from cashier.news.models import News
from cashier.payments.models import PaymentsAdmin
from tests.base.common import CashierTestCase


class NewsSignal(CashierTestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.create_superuser()

    def test_news_object_for_tax_only_created(self):
        previous_tax = PaymentsAdmin.objects.get(pk=1).individual_monthly_tax
        new_tax = PaymentsAdmin.objects.get(pk=1).individual_monthly_tax + 1
        admin_payment_profile = PaymentsAdmin.objects.get(pk=1)
        admin_payment_profile.individual_monthly_tax = new_tax
        admin_payment_profile.save()
        tax_message = f'The tax has changed from {previous_tax} to {new_tax}'
        self.assertTrue(News.objects.filter(title='Tax changed', content=tax_message).exists())
        self.assertFalse(News.objects.filter(title='Salaries changed').exists())

    def test_news_object_for_salary_only_created(self):
        previous_salary = PaymentsAdmin.objects.get(pk=1).salaries
        new_salary = PaymentsAdmin.objects.get(pk=1).salaries + 1
        admin_payment_profile = PaymentsAdmin.objects.get(pk=1)
        admin_payment_profile.salaries = new_salary
        admin_payment_profile.save()
        salaries_message = f'The salaries have changed from {previous_salary} to {new_salary}'
        self.assertFalse(News.objects.filter(title='Tax changed').exists())
        self.assertTrue(News.objects.filter(title='Salaries changed', content=salaries_message).exists())

    def test_news_object_for_both_tax_and_salary_created(self):
        previous_tax = PaymentsAdmin.objects.get(pk=1).individual_monthly_tax
        new_tax = PaymentsAdmin.objects.get(pk=1).individual_monthly_tax + 1
        previous_salary = PaymentsAdmin.objects.get(pk=1).salaries
        new_salary = PaymentsAdmin.objects.get(pk=1).salaries + 1
        admin_payment_profile = PaymentsAdmin.objects.get(pk=1)
        admin_payment_profile.individual_monthly_tax = new_tax
        admin_payment_profile.salaries = new_salary
        admin_payment_profile.save()
        tax_message = f'The tax has changed from {previous_tax} to {new_tax}'
        salaries_message = f'The salaries have changed from {previous_salary} to {new_salary}'

        self.assertTrue(News.objects.filter(title='Salaries changed', content=salaries_message).exists())
        self.assertTrue(News.objects.filter(title='Tax changed', content=tax_message).exists())