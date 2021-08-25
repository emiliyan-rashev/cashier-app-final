from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from cashier.profiles.models import UserProfile

UserModer = get_user_model()

class ContactDetailsObjectTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_profile_created_when_super_user_created(self):
        self.user = UserModer.objects.create_superuser(username='emo_superuser', password='123qwe')
        self.assertTrue(UserProfile.objects.filter(pk=self.user.id).exists())