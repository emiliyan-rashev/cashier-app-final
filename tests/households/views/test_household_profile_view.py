from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from cashier.households.models import HouseholdProfile
from cashier.profiles.models import UserProfile
from tests.base.common import CashierTestCase

UserModel = get_user_model()


class HouseholdProfileTest(CashierTestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.create_user(
            test_username="test1_username",
            test_email="test1_email@test.qwe",
            test_apartment=1,
        )
        self.create_user(
            test_username="test2_username",
            test_email="test2_email@test.qwe",
            test_apartment=1,
        )
        self.create_user(
            test_username="test3_username",
            test_email="test3_email@test.qwe",
            test_apartment=1,
        )
        self.create_user(
            test_username="test4_username",
            test_email="test4_email@test.qwe",
            test_apartment=1,
        )
        self.create_user(
            test_username="test5_username",
            test_email="test5_email@test.qwe",
            test_apartment=2,
        )
        self.user1 = UserModel.objects.get(username="test1_username")
        self.user2 = UserModel.objects.get(username="test2_username")
        self.user3 = UserModel.objects.get(username="test3_username")
        self.user4 = UserModel.objects.get(username="test4_username")
        self.user5 = UserModel.objects.get(username="test5_username")
        self.hh_profile = HouseholdProfile.objects.create(pk=1, apartment=1)
        self.second_hh_profile = HouseholdProfile.objects.create(pk=2, apartment=2)
        self.approve_user(self.user5)
        self.set_as_hh_admin(self.user5)

    def get_response(self):
        self.response = self.client.get(
            reverse("hh_profile", kwargs={"pk": self.hh_profile.apartment})
        )

    def approve_user(self, user):
        self.get_profile(user)
        profile = self.profile
        profile.household = HouseholdProfile.objects.get(pk=self.profile.apartment)
        profile.live_in_apartment = True
        profile.save()
        self.get_response()

    def remove_from_apartment(self, user):
        self.get_profile(user)
        profile = self.profile
        profile.live_in_apartment = False
        profile.save()
        self.get_response()

    def deactivate_user(self, user):
        user = user
        user.is_active = False
        user.save()
        self.get_response()

    def set_as_hh_admin(self, user):
        self.get_profile(user)
        profile = self.profile
        profile.is_household_admin = True
        profile.save()
        self.get_response()

    def remove_hh_admin(self, user):
        self.get_profile(user)
        profile = self.profile
        profile.is_household_admin = False
        profile.save()
        self.get_response()

    def test_get_initial_hh_info(self):
        # curr_user = UserProfile.objects.get(pk=self.request.user.id)
        self.assertTrue(self.response.context["household"] == self.hh_profile)
        self.assertListEmpty(list(self.response.context["members_in_hh"]))
        self.assertListEmpty(list(self.response.context["admins_in_hh"]))
        self.assertListEqual(
            list(self.response.context["not_approved_members"]),
            list(UserProfile.objects.filter(apartment=self.hh_profile.apartment)),
        )
        self.assertListEmpty(list(self.response.context["not_living_in_hh"]))

    def test_members_in_hh(self):
        self.approve_user(self.user1)
        self.assertListEqual(
            list(self.response.context["members_in_hh"]),
            list(UserProfile.objects.filter(user__in=[self.user1])),
        )

        self.approve_user(self.user2)
        self.assertListEqual(
            list(self.response.context["members_in_hh"]),
            list(UserProfile.objects.filter(user__in=[self.user1, self.user2])),
        )

        self.remove_from_apartment(self.user1)
        self.assertListEqual(
            list(self.response.context["members_in_hh"]),
            list(UserProfile.objects.filter(user__in=[self.user2])),
        )

        self.deactivate_user(self.user2)
        self.assertListEmpty(list(self.response.context["members_in_hh"]))

    def test_admins_in_hh(self):
        self.approve_user(self.user1)
        self.set_as_hh_admin(self.user1)
        self.assertListEqual(
            list(self.response.context["admins_in_hh"]),
            list(UserProfile.objects.filter(user__in=[self.user1])),
        )
        self.approve_user(self.user2)
        self.set_as_hh_admin(self.user2)
        self.remove_hh_admin(self.user1)
        self.assertListEqual(
            list(self.response.context["admins_in_hh"]),
            list(UserProfile.objects.filter(user__in=[self.user2])),
        )
        self.deactivate_user(self.user2)
        self.assertListEmpty(list(self.response.context["admins_in_hh"]))

    def test_not_approved_members(self):
        self.approve_user(self.user1)
        self.assertListEqual(
            list(self.response.context["not_approved_members"].order_by("user")),
            list(
                UserProfile.objects.filter(
                    user__in=[self.user2, self.user3, self.user4]
                ).order_by("user")
            ),
        )
        self.deactivate_user(self.user2)
        self.assertListEqual(
            list(self.response.context["not_approved_members"].order_by("user")),
            list(
                UserProfile.objects.filter(user__in=[self.user3, self.user4]).order_by(
                    "user"
                )
            ),
        )

    def test_not_living_in_hh(self):
        self.approve_user(self.user1)
        self.remove_from_apartment(self.user1)
        self.assertListEqual(
            list(self.response.context["not_living_in_hh"]),
            list(UserProfile.objects.filter(user__in=[self.user1])),
        )
        self.approve_user(self.user2)
        self.remove_from_apartment(self.user2)
        self.approve_user(self.user3)
        self.remove_from_apartment(self.user3)
        self.approve_user(self.user4)
        self.remove_from_apartment(self.user4)
        self.approve_user(self.user5)
        self.remove_from_apartment(self.user5)

        self.assertListEqual(
            list(self.response.context["not_living_in_hh"].order_by("user")),
            list(
                UserProfile.objects.filter(
                    user__in=[self.user1, self.user2, self.user3, self.user4]
                ).order_by("user")
            ),
        )

        self.set_as_hh_admin(self.user1)
        self.assertListEqual(
            list(self.response.context["not_living_in_hh"].order_by("user")),
            list(
                UserProfile.objects.filter(
                    user__in=[self.user1, self.user2, self.user3, self.user4]
                ).order_by("user")
            ),
        )
        self.approve_user(self.user1)
        self.assertListEqual(
            list(self.response.context["not_living_in_hh"].order_by("user")),
            list(
                UserProfile.objects.filter(
                    user__in=[self.user2, self.user3, self.user4]
                ).order_by("user")
            ),
        )
