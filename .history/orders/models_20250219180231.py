from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Customer(AbstractUser):  
    completename = models.CharField(max_length=250 )  
    phone_number = models.CharField(max_length=50 )  
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

BRAND_CHOICES = [
    ("Toyota", "Toyota"),
    ("Mitsubishi", "Mitsubishi"),
    ("Honda", "Honda"),
    ("Nissan", "Nissan"),
    ("Ford", "Ford"),
    ("Isuzu", "Isuzu"),
    ("Hyundai", "Hyundai"),
    ("Kia", "Kia"),
    ("Chevrolet", "Chevrolet"),
    ("Suzuki", "Suzuki"),
    ("Daihatsu", "Daihatsu"),
    ("Mazda", "Mazda"),
    ("Subaru", "Subaru"),
    ("Fuso", "Fuso"),
    ("Hino", "Hino"),
    ("Tata", "Tata"),
    ("MAN", "MAN"),
    ("Scania", "Scania"),
    ("Volkswagen", "Volkswagen"),
    ("Chery", "Chery"),
    ("Foton", "Foton"),
    ("JAC", "JAC"),
    ("Dongfeng", "Dongfeng"),
    ("Changan", "Changan"),
    ("Geely", "Geely"),
    ("MG", "MG"),
    ("BYD", "BYD"),
    ("BAIC", "BAIC"),
    ("GAC", "GAC"),
    ("Maxus", "Maxus"),
]

STATUS_CHOICES = [
    ("Open", "Open"),
    ("Closed", "Closed"),
]

# Part Request Model
class PartRequest(models.Model):
    brand_new = models.BooleanField(default=True)
    used = models.BooleanField(default=False)
    
   
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    part_name = models.CharField(max_length=255)
    description = models.TextField()
    qty = models.PositiveIntegerField(default="1")
    image1 = models.ImageField(upload_to="part_images/")
    image2 = models.ImageField(upload_to="part_images/")
    brand = models.CharField(max_length=255, choices=BRAND_CHOICES)
    year = models.PositiveIntegerField()
    car_model = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Open")
    
    def __str__(self):
        return f"{self.part_name} ({self.brand} - {self.car_model})"
    
    
    from django.db import models
from django.conf import settings

# Bid Status Choices
BID_STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Accepted", "Accepted"),
    ("Rejected", "Rejected"),
]
CONDITION_CHOICES = [
    ("Brand New", "Brand New"),
    ("Used", "Used"),
    
]
from django.db import models
from django.conf import settings

class Bid(models.Model):
    part_request = models.ForeignKey("orders.PartRequest", on_delete=models.CASCADE, related_name="bids")
    store = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default="Brand New")  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    image1 = models.ImageField(upload_to="bid_images/", blank=True, null=True)
    image2 = models.ImageField(upload_to="bid_images/", blank=True, null=True)
    status = models.CharField(max_length=10, choices=BID_STATUS_CHOICES, default="Pending")    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid by {self.store.username} for {self.part_request.part_name}"

