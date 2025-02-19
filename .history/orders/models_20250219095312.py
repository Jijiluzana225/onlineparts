from django.contrib.auth.models import AbstractUser
from django.db import models

class Customer(AbstractUser):  
    completename = models.CharField(max_length=250, unique=True)  
    phone_number = models.CharField(max_length=15, unique=True)  
    address = models.TextField(blank=True, null=True)
    

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customer_users",  # Custom related name to avoid conflicts
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customer_users_permissions",  # Custom related name
        blank=True
    )

    def __str__(self):
        return self.username
