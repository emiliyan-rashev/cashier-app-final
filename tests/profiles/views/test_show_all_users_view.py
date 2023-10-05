from django.urls import reverse
from cashier.profiles.models import UserProfile
from tests.base.common import CashierTestCase


class ShowAllUsersViewTest(CashierTestCase):
    def test_users_queryset(self):
        self.create_superuser()
        self.client.force_login(self.super_user)
        response = self.client.get(reverse("all_users"))

        self.assertListEqual(
            list(response.context["all_users"]),
            list(UserProfile.objects.filter(apartment__isnull=False)),
        )
