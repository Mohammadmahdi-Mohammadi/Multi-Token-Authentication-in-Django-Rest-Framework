from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    # Phone = models.CharField(max_length=12,unique=True, blank=False)
    Phone = PhoneNumberField(blank=False,unique=True)
    Phone_verify = models.BooleanField(null=True,blank=True)
    OTP = models.CharField(max_length=4,blank=True,null=True)
    provider = models.CharField(max_length=20,blank=True,null=True)
    counter = models.IntegerField(default=1)




