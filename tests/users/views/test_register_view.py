from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from cashier.profiles.models import UserProfile
from cashier.users.forms import UserForm

UserModel = get_user_model()


class RegisterViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

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
        test_username = 'test_username'
        test_password = 'test_password'
        test_first_name = 'test_first_name'
        test_last_name = 'test_last_name'
        test_email = 'test_email@test.qwe'
        test_phone_number = '0123456789'
        test_apartment = 1
        test_live_in_apartment = True
        test_newsletter_agreement = True
        response = self.client.post(reverse('register_view'), data={
                'username' : test_username,
                'password1' : test_password,
                'password2' : test_password,
                'first_name' : test_first_name,
                'last_name' : test_last_name,
                'email' : test_email,
                'phone_number' : test_phone_number,
                'apartment' : test_apartment,
                'live_in_apartment' : test_live_in_apartment,
                'newsletter_agreement' : test_newsletter_agreement,
            }
        )
        user_id = response.wsgi_request.user.id
        user = UserModel.objects.get(pk=user_id)
        profile = UserProfile.objects.get(pk=user_id)

        self.assertEqual(user.username, test_username)
        self.assertEqual(profile.first_name, test_first_name)
        self.assertEqual(profile.last_name, test_last_name)
        self.assertEqual(profile.email, test_email)
        self.assertEqual(profile.phone_number, test_phone_number)
        self.assertEqual(profile.apartment, test_apartment)
        self.assertIsNone(profile.household)
        self.assertEqual(profile.live_in_apartment, test_live_in_apartment)
        self.assertEqual(profile.newsletter_agreement, test_newsletter_agreement)
        self.assertFalse(profile.is_household_admin)
        self.assertEqual(profile.user, user)

