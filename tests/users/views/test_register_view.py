from django.urls import reverse
from tests.base.common import CashierTestCase


class RegisterViewTest(CashierTestCase):

    def test_both_user_and_profile_forms_are_loaded(self):
        response = self.client.get(reverse('register_view'))
        self.assertTrue(response.context['user_form'].__class__.__name__ == 'UserForm')
        self.assertTrue(response.context['profile_form'].__class__.__name__ == 'EditProfileForm')

    def test_user_form_fields_are_correct(self):
        response = self.client.get(reverse('register_view'))
        self.assertListEqual(list(response.context['user_form'].fields.keys()), ['username', 'password1', 'password2'])

    def test_profile_form_fields_are_correct(self):
        response = self.client.get(reverse('register_view'))
        profile_form_shown_fields = ['first_name', 'last_name', 'email', 'phone_number', 'apartment', 'live_in_apartment', 'newsletter_agreement']
        self.assertListEqual(list(response.context['profile_form'].fields.keys()), profile_form_shown_fields)

    def test_user_and_profile_creation(self):
        self.create_user()
        self.assertEqual(self.user.username, self.test_username)
        self.assertEqual(self.profile.first_name, self.test_first_name)
        self.assertEqual(self.profile.last_name, self.test_last_name)
        self.assertEqual(self.profile.email, self.test_email)
        self.assertEqual(self.profile.phone_number, self.test_phone_number)
        self.assertEqual(self.profile.apartment, self.test_apartment)
        self.assertIsNone(self.profile.household)
        self.assertEqual(self.profile.live_in_apartment, self.test_live_in_apartment)
        self.assertEqual(self.profile.newsletter_agreement, self.test_newsletter_agreement)
        self.assertFalse(self.profile.is_household_admin)
        self.assertEqual(self.profile.user, self.user)

