from django.urls import path

from news.views import (
    NewsListView,
    CommentNewsView,
    DeleteCommentView,
    CreateNews,
)

urlpatterns = [
    path("", NewsListView.as_view(), name="all_news_view"),
    path("<int:pk>", CommentNewsView.as_view(), name="comment_news_view"),
    path("delete/comment/<int:pk>", DeleteCommentView.as_view(), name="delete_comment"),
    path("create/", CreateNews.as_view(), name="create_news"),
]
