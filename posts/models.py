from django.conf import settings

from account.models import User

from django.db import models
from django.conf import settings
from django.db import models

from rest_framework.authtoken.models import Token


class Post(models.Model):
    auth = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField(blank = True)
    is_enable = models.BooleanField(default=False)
    publish_date = models.DateField(null = True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now= True)

    def __str__(self):
        #return self.title
        return '{}- {}'.format(self.pk , self.title)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add = True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        #return self.title
        return '{}- {}'.format(self.pk , self.text)


class ExtendedUserExample(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    phone_number = models.IntegerField(blank=True)


class MultiTokens(Token):
    # key is no longer primary key, but still indexed and unique
    key = models.CharField("Key", max_length=40, db_index=True, unique=True)
    # relation to user is a ForeignKey, so each user can have more than one token
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='auth_tokens',
        on_delete=models.CASCADE, verbose_name="User" )
    name = models.CharField("Name", max_length=64)
    counterplus = models.IntegerField(default=0)

    class Meta:
        unique_together = (('user', 'counterplus'),)



