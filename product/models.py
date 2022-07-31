from django.db import models
from  account.models import User
# from django.contrib.sites.models import Site

class Product(models.Model):
    name = models.CharField(max_length=100)
    count = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)
    number_of_voters = models.IntegerField(default=0)
    def __str__(self):
        return self.name
    # def __init__(self):
    #     user_array = []


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_add = models.DateTimeField(auto_now_add=True)
    chech_admin = models.BooleanField(default=False)

    def __str__(self):
        return  '{}- {}'.format(self.pk, self.body)
