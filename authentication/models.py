from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from datetime import datetime
import clearbit
import json
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        # Ensure that an email address is set
        if not email:
            raise ValueError('Users must have a valid e-mail address')
        # Ensure that a username is set
        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username')
        clearbit.key = 'sk_a58ce3ff299332066447fe9eba0f0543'
        lookup = clearbit.Enrichment.find(email=email, stream=True)
        if lookup != None:
            enrichjson = json.dumps(lookup['person'], sort_keys=True, indent=4)
            enrichjson = enrichjson.rstrip('\n')
        else:
            enrichjson = 'NotFound'
        user = self.model(
            email=self.normalize_email(email),
            username=kwargs.get('username'),
            enrichjson= enrichjson,
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(email, password, kwargs)

        user.is_admin = True
        user.save()

        return user


class User(AbstractBaseUser):
    enrichjson = models.CharField(max_length=8000, default='None')
    username = models.CharField(unique=True, max_length=50)
    email = models.EmailField(unique=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.now())
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=1000)
    date = models.DateTimeField('date published')
    likers = models.ManyToManyField(User,related_name='likerslist')
    def __str__(self):
        return self.title
    def was_published_recently(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)
    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk' : self.pk})

'''class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField('date liked')'''
