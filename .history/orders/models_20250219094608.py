from django.contrib.auth.models import AbstractUser
from django.db import models

class Customer(AbstractUser):  
    phone_number = models.CharField(max_length=15, unique=True)  
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
