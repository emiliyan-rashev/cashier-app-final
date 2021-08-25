from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from cashier.profiles.models import UserProfile

UserModel = get_user_model()

class ShowAllUsersViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_users_queryset(self):
        self.user = UserModel.objects.create_superuser(username='emo_superuser', password='123qwe')
        self.client.force_login(self.user)

        response = self.client.get(reverse('all_users'))

        self.assertListEqual(list(response.context['all_users']), list(UserProfile.objects.filter(apartment__isnull=False)))
