from django.test import Client

from cashier.payments.models import IndividualPayment, IndividualTaxesPayed
from tests.base.common import CashierTestCase


class ProfileUpdated(CashierTestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.create_user()

    def test_payment_profile_created(self):
        self.assertTrue(IndividualPayment.objects.get(pk=self.user.id))

    def test_individual_taxes_paid_created(self):
        self.assertTrue(IndividualTaxesPayed.objects.get(pk=self.user.id))