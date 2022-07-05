from django.db import models

from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    # Phone = models.CharField(max_length=12,unique=True, blank=False)
    Phone = PhoneNumberField(unique=True, blank=False)





