import datetime
from django.test import Client


class PaySalariesAndTaxes:
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
        self.target = None
        self.tax_class_object = None
        self.paid_class_object = None

    def tearDown(self) -> None:
        self.tax_class_object.update(**{month: 0 for month in self.month_keys})
        self.paid_class_object.objects.filter(pk=1).update(
            **{month: 0 for month in self.month_keys}
        )

    def pay_first_month(self):
        self.client.post(
            self.target,
            data={
                str(self.month_keys[0]): True,
            },
        )

    def pay_last_month(self):
        self.client.post(
            self.target,
            data={
                str(self.month_keys[-1]): True,
            },
        )

    def pay_all_months(self):
        self.client.post(self.target, data={month: True for month in self.month_keys})

    def get_context_data(self):
        self.response = self.client.get(self.target)
        self.context_months = [
            curr_row[0] for curr_row in self.response.context["tax_info"]
        ]
        self.context_taxes_needed_per_month = [
            curr_row[1] for curr_row in self.response.context["tax_info"]
        ]
        self.context_taxes_paid_per_month = [
            curr_row[2] for curr_row in self.response.context["tax_info"]
        ]

        self.context_sum_of_taxes_needed = self.response.context["total_taxes_needed"]
        self.context_sum_of_taxes_paid = self.response.context["total_taxes_paid"]

    def test_form_initial_fields(self):
        self.get_form_field_names(self.target)
        self.assertListEmpty(self.displayed_fields)

    def test_form_fields_after_payment(self):
        self.tax_class_object.update(**{month: 1 for month in self.month_keys})
        self.pay_first_month()
        self.get_form_field_names(self.target)
        self.assertListEqual(self.displayed_fields, self.month_keys[1:])

        self.pay_last_month()
        self.get_form_field_names(self.target)
        self.assertListEqual(self.displayed_fields, self.month_keys[1:-1])

        self.pay_all_months()
        self.get_form_field_names(self.target)
        self.assertListEmpty(self.displayed_fields)

    def test_form_fields_after_increasing_the_salary(self):
        self.tax_class_object.update(**{month: 1 for month in self.month_keys})
        self.pay_first_month()
        self.tax_class_object.update(**{month: 2 for month in self.month_keys})
        self.get_form_field_names(self.target)

        self.assertListEqual(self.displayed_fields, self.month_keys)

        self.pay_all_months()
        self.tax_class_object.update(**{month: 3 for month in self.month_keys})
        self.get_form_field_names(self.target)

        self.assertListEqual(self.displayed_fields, self.month_keys)

    def test_form_fields_after_decreasing_the_salary(self):
        self.tax_class_object.update(**{month: 4 for month in self.month_keys})
        self.pay_first_month()
        self.tax_class_object.update(**{month: 3 for month in self.month_keys})
        self.get_form_field_names(self.target)
        self.assertListEqual(self.displayed_fields, self.month_keys[1:])

        self.pay_last_month()
        self.tax_class_object.update(**{month: 2 for month in self.month_keys})
        self.get_form_field_names(self.target)
        self.assertListEqual(self.displayed_fields, self.month_keys[1:-1])

        self.pay_all_months()
        self.tax_class_object.update(**{month: 1 for month in self.month_keys})
        self.get_form_field_names(self.target)
        self.assertListEmpty(self.displayed_fields)

    def test_get_context_data(self):
        self.get_context_data()

        self.assertListEqual(self.context_months, self.month_keys)
        zero_full_arr = [0 for x in range(12)]
        self.assertListEqual(self.context_taxes_needed_per_month, zero_full_arr)
        self.assertListEqual(self.context_taxes_paid_per_month, zero_full_arr)

        self.tax_class_object.update(**{month: 1 for month in self.month_keys})
        self.pay_first_month()
        self.get_context_data()

        self.assertListEqual(
            self.context_taxes_needed_per_month, [1 for x in range(12)]
        )
        self.assertListEqual(self.context_taxes_paid_per_month, [1] + zero_full_arr[1:])

        self.pay_last_month()
        self.get_context_data()

        self.assertListEqual(
            self.context_taxes_needed_per_month, [1 for x in range(12)]
        )
        self.assertListEqual(
            self.context_taxes_paid_per_month, [1] + zero_full_arr[1:-1] + [1]
        )

        self.tax_class_object.update(**{month: 3 for month in self.future_months})
        self.get_context_data()
        expected_taxes = [1 for x in range(12 - len(self.future_months))] + [
            3 for x in self.future_months
        ]
        self.assertListEqual(self.context_taxes_needed_per_month, expected_taxes)
