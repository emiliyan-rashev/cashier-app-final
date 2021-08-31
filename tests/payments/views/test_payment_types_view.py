from django.urls import reverse
from tests.base.common import CashierTestCase


class PaymentTypesTest(CashierTestCase):
    # Test is too complicated - includes too much actions
    def test_get(self):
        self.create_user()
        self.client.force_login(self.user)
        response = self.client.get(reverse('payment_types'))

        self.assertFalse(response.context['is_hh_admin'])
        self.assertEqual(self.profile.apartment, response.context['apartment'])

        self.create_superuser()
        self.client.logout()
        self.client.force_login(self.super_user)
        self.client.post(reverse('hh_approve_user', kwargs={'pk': self.user.id}), data={'approval': 'Approve'})
        self.client.post(reverse('set_hh_admin', kwargs={'pk': self.user.id}), data={'is_household_admin': True})
        self.client.logout()
        self.client.force_login(self.user)

        response = self.client.get(reverse('payment_types'))

        self.assertTrue(response.context['is_hh_admin'])
        self.assertEqual(self.profile.apartment, response.context['apartment'])
