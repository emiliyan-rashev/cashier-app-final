from django.contrib.auth import get_user_model
from django.test import Client

from cashier.payments.models import (
    PaymentsAdmin,
    TaxesPerMonth,
    SalariesPerMonth,
    SalariesPayedPerMonth,
    SalariesPayment,
)
from tests.base.common import CashierTestCase

UserModel = get_user_model()


class SuperuserCreated(CashierTestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.create_superuser()

    def tearDown(self) -> None:
        UserModel.objects.all().delete()

    def test_payments_admin_created(self):
        self.assertTrue(PaymentsAdmin.objects.exists())

    def test_taxes_per_month_created(self):
        self.assertTrue(TaxesPerMonth.objects.exists())

    def test_salaries_per_month_created(self):
        self.assertTrue(SalariesPerMonth.objects.exists())

    def test_salaries_payed_per_month_created(self):
        self.assertTrue(SalariesPayedPerMonth.objects.exists())

    def test_salaries_payment_created(self):
        self.assertTrue(SalariesPayment.objects.exists())
