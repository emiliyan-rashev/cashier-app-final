from django.urls import reverse
from cashier.users.models import ContactDetails
from tests.base.common import CashierTestCase


class ContactDetailsTest(CashierTestCase):
    def test_get_when_contact_object_does_not_exist(self):
        response = self.client.get(reverse("contact_view"))
        context_keys = response.context.keys()

        self.assertTrue("email" not in context_keys)
        self.assertTrue("phone" not in context_keys)
        self.assertTrue("first_name" not in context_keys)
        self.assertTrue("last_name" not in context_keys)

    def test_get_when_contact_object_exists(self):
        self.create_superuser()
        contact_object = ContactDetails.objects.get(pk=1)
        contact_object.email = "test_email"
        contact_object.phone = "test_phone"
        contact_object.first_name = "test_first_name"
        contact_object.last_name = "test_last_name"
        contact_object.save()
        response = self.client.get(reverse("contact_view"))
        context = response.context

        self.assertTrue(context["email"] == "test_email")
        self.assertTrue(context["phone"] == "test_phone")
        self.assertTrue(context["first_name"] == "test_first_name")
        self.assertTrue(context["last_name"] == "test_last_name")
