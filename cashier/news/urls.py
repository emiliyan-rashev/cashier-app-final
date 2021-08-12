from django.urls import path

from cashier.news.views import NewsListView, CommentNewsView, DeleteCommentView

urlpatterns = [
    path('', NewsListView.as_view(), name='all_news_view'),
    path('<int:pk>', CommentNewsView.as_view(), name='comment_news_view'),
    path('delete/comment/<int:pk>', DeleteCommentView.as_view(), name='delete_comment'),
]