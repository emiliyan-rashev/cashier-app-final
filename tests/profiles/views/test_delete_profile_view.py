from django.test import Client
from django.urls import reverse

from tests.base.common import CashierTestCase


class DeleteProfileViewTest(CashierTestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.create_user()
        self.client.force_login(user=self.user)

    def test_profile_owner(self):
        response = self.client.get(reverse('delete_profile', kwargs={'pk': self.user_id}))
        self.assertTrue(response.context['profile_owner'])

    def test_user_deactivation__profile_apartment_and_household_update(self):
        self.client.post(reverse('delete_profile', kwargs={'pk': self.user_id}), data={'result' : 'Delete'})
        self.get_user(pk=self.user_id)
        self.get_profile(pk=self.user_id)
        self.assertFalse(self.user.is_active)
        self.assertIsNone(self.profile.apartment)
        self.assertIsNone(self.profile.household)
        self.assertFalse(self.profile.live_in_apartment)