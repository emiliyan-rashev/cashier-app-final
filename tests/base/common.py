from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from cashier.profiles.models import UserProfile

UserModel = get_user_model()

class CashierTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def assertListEmpty(self, my_list):
        return self.assertListEqual([], my_list, 'List is not empty')

    def create_user(self):
        self.test_username = 'test_username'
        self.test_password = 'test_password'
        self.test_first_name = 'test_first_name'
        self.test_last_name = 'test_last_name'
        self.test_email = 'test_email@test.qwe'
        self.test_phone_number = '0123456789'
        self.test_apartment = 1
        self.test_live_in_apartment = True
        self.test_newsletter_agreement = True
        self.response = self.client.post(reverse('register_view'), data={
            'username': self.test_username,
            'password1': self.test_password,
            'password2': self.test_password,
            'first_name': self.test_first_name,
            'last_name': self.test_last_name,
            'email': self.test_email,
            'phone_number': self.test_phone_number,
            'apartment': self.test_apartment,
            'live_in_apartment': self.test_live_in_apartment,
            'newsletter_agreement': self.test_newsletter_agreement,
        }
                                    )
        self.user_id = self.response.wsgi_request.user.id
        self.get_user(pk=self.user_id)
        self.get_profile(pk=self.user_id)

    def create_superuser(self):
        self.super_user = UserModel.objects.create_superuser(username='emo_superuser', password='123qwe')

    def get_user(self, pk):
        self.user = UserModel.objects.get(pk=pk)

    def get_profile(self, pk):
        self.profile = UserProfile.objects.get(pk=pk)

    def get_form_field_names(self, view_name):
        self.displayed_fields = list(self.client.get(view_name).context['form'].fields.keys())