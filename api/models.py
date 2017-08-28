from django.db import models
# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class User(AbstractUser):
    enrichjson = models.CharField(max_length=8000, default='None')


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=1000)
    date = models.DateTimeField('date published')
    def __str__(self):
        return self.title
    def was_published_recently(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)
    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk' : self.pk})

class Like(models.Model):
    User = models.ForeignKey(User)
    Post = models.ForeignKey(Post)
    created = models.DateTimeField(auto_now_add=True)
