from django.test import Client
from django.urls import reverse

from cashier.news.models import News, Comment
from tests.base.common import CashierTestCase


class DeleteNewsTest(CashierTestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.create_user()
        self.client.force_login(self.user)
        self.title = "test_title"
        self.content = "test_content"
        self.news = News.objects.create(title=self.title, content=self.content)

    def test_get_without_any_comments(self):
        response = self.client.get(
            reverse("comment_news_view", kwargs={"pk": self.news.id})
        )
        self.assertListEmpty(list(response.context["all_comments"]))

    def test_get_with_comments(self):
        Comment.objects.create(content=self.content, News=self.news, user=self.user)
        response = self.client.get(
            reverse("comment_news_view", kwargs={"pk": self.news.id})
        )
        self.assertListEqual(
            list(response.context["all_comments"]),
            list(
                Comment.objects.filter(
                    content=self.content, News=self.news, user=self.user
                )
            ),
        )

    def test_post(self):
        self.client.post(
            reverse("comment_news_view", kwargs={"pk": self.news.id}),
            data={"content": self.content},
        )
        response = self.client.get(
            reverse("comment_news_view", kwargs={"pk": self.news.id})
        )
        self.assertListEqual(
            list(response.context["all_comments"]),
            list(
                Comment.objects.filter(
                    content=self.content, News=self.news, user=self.user
                )
            ),
        )
