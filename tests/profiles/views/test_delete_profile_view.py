from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from cashier.profiles.models import UserProfile

UserModel = get_user_model()

class DeleteProfileViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        test_username = 'test_username'
        test_password = 'test_password'
        test_first_name = 'test_first_name'
        test_last_name = 'test_last_name'
        test_email = 'test_email@test.qwe'
        test_phone_number = '0123456789'
        test_apartment = 11
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
        self.user_id = response.wsgi_request.user.id
        self.user = UserModel.objects.get(pk=self.user_id)
        self.client.force_login(user=self.user)
        self.profile = UserProfile.objects.get(pk=self.user_id)

    def test_profile_owner(self):
        response = self.client.get(reverse('delete_profile', kwargs={'pk': self.user_id}))
        self.assertTrue(response.context['profile_owner'])

    def test_user_deactivation__profile_apartment_and_household_update(self):
        self.client.post(reverse('delete_profile', kwargs={'pk': self.user_id}), data={'result' : 'Delete'})
        #To be set as getter
        self.user = UserModel.objects.get(pk=self.user_id)
        self.profile = UserProfile.objects.get(pk=self.user_id)

        self.assertFalse(self.user.is_active)
        self.assertIsNone(self.profile.apartment)
        self.assertIsNone(self.profile.household)
        self.assertFalse(self.profile.live_in_apartment)