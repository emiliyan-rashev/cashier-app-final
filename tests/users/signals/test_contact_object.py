from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from cashier.users.models import ContactDetails

UserModer = get_user_model()

class CashierTestCase(TestCase):
    def assertListEmpty(self, my_list):
        return self.assertListEqual([], my_list, 'List is not empty')

class ContactDetailsObjectTest(CashierTestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_signal_for_ContactView_object_on_super_user_creation(self):
        self.assertListEmpty(list(ContactDetails.objects.all()))
        UserModer.objects.create_superuser(username='emo_superuser', password='123qwe')
        self.assertTrue(list(ContactDetails.objects.all()))