from django.conf import settings

from account.models import User
from django.db import models

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




