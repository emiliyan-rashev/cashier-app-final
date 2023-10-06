from profiles.models import UserProfile
from tests.base.common import CashierTestCase


class ContactDetailsObjectTest(CashierTestCase):
    def test_profile_created_when_super_user_created(self):
        self.create_superuser()
        self.assertTrue(UserProfile.objects.filter(pk=self.super_user.id).exists())
