from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

class Customer(AbstractUser):  
    completename = models.CharField(max_length=250, unique=True)  
    phone_number = models.CharField(max_length=15, unique=True)  
    address = models.TextField(blank=True, null=True)
    is_store = models.BooleanField(default=False)
    
    
    
    

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


class PartRequest(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="part_requests")
    part_name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="part_images/")
    car_model = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    brand = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.part_name