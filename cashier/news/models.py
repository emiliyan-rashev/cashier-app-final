from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()

class News(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField(max_length=1000)

class Comment(models.Model):
    content = models.TextField(verbose_name='Comment', max_length=200)
    News = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)