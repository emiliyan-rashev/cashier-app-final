import datetime

from django.test import Client
from django.urls import reverse

from cashier.payments.models import TaxesPerMonth, IndividualTaxesPayed
from tests.base.common import CashierTestCase
from tests.payments.common.taxes_and_salaries_payments import PaySalariesAndTaxes


class PayTaxes(CashierTestCase, PaySalariesAndTaxes):
    def setUp(self) -> None:
        self.client = Client()
        self.create_superuser()
        self.create_user()
        self.client.force_login(self.user)
        self.month_keys = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.curr_month = datetime.date.today().month
        self.future_months = self.month_keys[self.curr_month:len(self.month_keys)]
        self.target = reverse('make_payment', kwargs={'pk': self.user_id})
        self.tax_class_object = TaxesPerMonth.objects.filter(pk=1)
        self.paid_class_object = IndividualTaxesPayed.objects.filter(pk=self.user_id)
