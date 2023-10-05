from django.contrib.auth import get_user_model
from django.db.models import Q
from django.test import Client
from django.urls import reverse

from cashier.households.models import HouseholdProfile
from cashier.profiles.models import UserProfile
from tests.base.common import CashierTestCase

UserModel = get_user_model()


class UrgentPendingMembersTest(CashierTestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.create_superuser()
        self.create_user()

    def test_when_hh_object_does_not_exist(self):
        self.client.force_login(self.super_user)
        response = self.client.get(reverse("urgent_pending_members"))
        self.assertListEmpty(list(response.context["existing_apartments"]))
        self.assertListEqual(
            list(response.context["not_approved_members"]),
            list(UserProfile.objects.filter(user=self.user)),
        )

    def test_user_with_hh_admin_not_appearing(self):
        hh_profile = HouseholdProfile(
            pk=self.profile.apartment, apartment=self.profile.apartment
        )
        hh_profile.save()
        profile = self.profile
        profile.household = hh_profile
        profile.is_household_admin = True
        profile.save()
        self.create_user(
            test_username="test_2", test_email="test2_email@test.qwe", test_apartment=1
        )
        self.client.force_login(self.super_user)
        response = self.client.get(reverse("urgent_pending_members"))
        self.assertListEqual(list(response.context["existing_apartments"]), [1])
        self.assertListEmpty(list(response.context["not_approved_members"]))

    def test_two_users_in_the_same_hh_without_having_hh_admin(self):
        self.create_user(
            test_username="test_3", test_email="test3_email@test.qwe", test_apartment=1
        )
        self.client.force_login(self.super_user)
        response = self.client.get(reverse("urgent_pending_members"))

        self.assertListEmpty(list(response.context["existing_apartments"]))
        self.assertListEqual(
            list(response.context["not_approved_members"]),
            list(UserProfile.objects.filter(~Q(user=self.super_user))),
        )

    def test_when_another_user_is_in_hh_but_is_not_admin(self):
        hh_profile = HouseholdProfile(
            pk=self.profile.apartment, apartment=self.profile.apartment
        )
        hh_profile.save()
        profile = self.profile
        profile.household = hh_profile
        profile.is_household_admin = False
        profile.save()
        self.create_user(
            test_username="test_2", test_email="test2_email@test.qwe", test_apartment=1
        )
        self.client.force_login(self.super_user)
        response = self.client.get(reverse("urgent_pending_members"))
        self.assertListEqual(list(response.context["existing_apartments"]), [1])
        self.assertListEqual(
            list(response.context["not_approved_members"]),
            list(UserProfile.objects.filter(user=self.user)),
        )

    def test_inactive_users_not_shown(self):
        user = self.user
        user.is_active = False
        user.save()
        self.client.force_login(self.super_user)
        response = self.client.get(reverse("urgent_pending_members"))
        self.assertListEmpty(list(response.context["existing_apartments"]))
        self.assertListEmpty(list(response.context["not_approved_members"]))
