from django.db import models

from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    # Phone = models.CharField(max_length=12,unique=True, blank=False)
    Phone = PhoneNumberField(blank=False,unique=True)
    OTP = models.CharField(max_length=4,blank=True,null=True)
    created_time = models.IntegerField(blank=True,null=True)
    Phone_verify = models.BooleanField(null=True,blank=True)
    # pass




