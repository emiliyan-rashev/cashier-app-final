import datetime

from django.test import Client
from django.urls import reverse

from cashier.payments.models import TaxesPerMonth, SalariesPerMonth
from tests.base.common import CashierTestCase


class AdminTaxUpdateTest(CashierTestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.create_superuser()
        self.client.force_login(self.super_user)
        self.month_keys = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        self.curr_month = datetime.date.today().month
        self.future_months = self.month_keys[self.curr_month : len(self.month_keys)]

    def test_tax_update(self):
        self.client.post(
            reverse("payments_admin"), data={"individual_monthly_tax": 1, "salaries": 1}
        )
        tax_object = TaxesPerMonth.objects.first()
        self.assertTrue(
            all(
                [
                    curr_field.value_from_object(tax_object) == 0
                    for curr_field in tax_object._meta.get_fields()
                    if (
                        not curr_field.name in self.future_months
                        and curr_field.name in self.month_keys
                    )
                ]
            )
        )
        self.assertTrue(
            all(
                [
                    curr_field.value_from_object(tax_object) == 1
                    for curr_field in tax_object._meta.get_fields()
                    if curr_field.name in self.future_months
                ]
            )
        )

        salary_object = SalariesPerMonth.objects.first()
        self.assertTrue(
            all(
                [
                    curr_field.value_from_object(salary_object) == 0
                    for curr_field in salary_object._meta.get_fields()
                    if (
                        not curr_field.name in self.future_months
                        and curr_field.name in self.month_keys
                    )
                ]
            )
        )
        self.assertTrue(
            all(
                [
                    curr_field.value_from_object(salary_object) == 1
                    for curr_field in salary_object._meta.get_fields()
                    if curr_field.name in self.future_months
                ]
            )
        )
