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


# Part Request Model
class PartRequest(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="part_requests",
        limit_choices_to={"is_customer": True}  # Ensures only customers can request
    )
    part_name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="part_images/")
    brand = models.CharField(max_length=255, choices=BRAND_CHOICES)
    year = models.PositiveIntegerField()
    car_model = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.part_name} ({self.brand} - {self.car_model})"