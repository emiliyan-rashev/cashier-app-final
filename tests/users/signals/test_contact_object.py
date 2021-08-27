from cashier.users.models import ContactDetails
from tests.base.common import CashierTestCase


class ContactDetailsObjectTest(CashierTestCase):
    def test_signal_for_ContactView_object_on_super_user_creation(self):
        self.assertListEmpty(list(ContactDetails.objects.all()))
        self.create_superuser()
        self.assertTrue(list(ContactDetails.objects.all()))