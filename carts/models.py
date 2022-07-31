from django.db import models
from account.models import User
from product.models import Product
from product.models import Product
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # ordered = models.BooleanField(default=True)
    # total_price = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    def __str__(self):

        return str(self.product) + "//"+ str(self.count)