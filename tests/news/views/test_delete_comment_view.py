from django.test import Client
from django.urls import reverse

from cashier.news.models import News, Comment
from tests.base.common import CashierTestCase


class DeleteNewsTest(CashierTestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.create_user()
        self.create_superuser()
        self.title = 'test_title'
        self.content = 'test_content'
        self.news = News.objects.create(title=self.title, content=self.content)

    def test_get_when_owner_or_superuser(self):
        self.client.force_login(self.user)
        comment = Comment.objects.create(content=self.content, News=self.news, user=self.user)
        response = self.client.get(reverse('delete_comment', kwargs={'pk': comment.id}))
        self.assertTrue(response.status_code == 200)
        self.client.logout()
        self.client.force_login(self.super_user)
        response = self.client.get(reverse('delete_comment', kwargs={'pk': comment.id}))
        self.assertTrue(response.status_code == 200)

    def test_get_when_not_owner(self):
        self.client.force_login(self.super_user)
        comment = Comment.objects.create(content=self.content, News=self.news, user=self.super_user)
        self.client.logout()
        self.client.force_login(self.user)
        response = self.client.get(reverse('delete_comment', kwargs={'pk': comment.id}))
        self.assertTrue(response.status_code == 302)
