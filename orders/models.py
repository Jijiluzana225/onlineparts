from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from cloudinary_storage.storage import MediaCloudinaryStorage
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils import timezone



class Customer(AbstractUser):  
    completename = models.CharField(max_length=250)  
    phone_number = models.CharField(max_length=50)  
    address = models.TextField(blank=True, null=True)
    is_store = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customer_users",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customer_users_permissions",
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


def resize_image_to_400x400(image_field):
    """
    Resize image to 400x400px and return as ContentFile
    Works with Cloudinary storage
    """
    if not image_field:
        return image_field
    
    try:
        # Open the image
        img = Image.open(image_field)
        
        # Convert RGBA to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img
        
        # Thumbnail maintains aspect ratio
        img.thumbnail((400, 400), Image.Resampling.LANCZOS)
        
        # Create a new 400x400 image with white background
        final_img = Image.new('RGB', (400, 400), (255, 255, 255))
        
        # Calculate offset to center the image
        offset = ((400 - img.size[0]) // 2, (400 - img.size[1]) // 2)
        final_img.paste(img, offset)
        
        # Save to BytesIO
        img_io = BytesIO()
        final_img.save(img_io, format='JPEG', quality=85, optimize=True)
        img_io.seek(0)
        
        # Get original filename
        original_name = image_field.name if hasattr(image_field, 'name') else 'image.jpg'
        
        # Return ContentFile
        return ContentFile(img_io.read(), name=original_name)
    except Exception as e:
        print(f"Error resizing image: {e}")
        return image_field


class PartRequest(models.Model):
    brand_new = models.BooleanField(default=True)
    used = models.BooleanField(default=False)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    part_name = models.CharField(max_length=255)
    description = models.TextField()
    qty = models.PositiveIntegerField(default=1)
    image1 = models.ImageField(storage=MediaCloudinaryStorage(), upload_to="part_images/")
    image2 = models.ImageField(storage=MediaCloudinaryStorage(), upload_to="part_images/")
    brand = models.CharField(max_length=255, choices=BRAND_CHOICES)
    year = models.PositiveIntegerField()
    car_model = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Open")
    
    def save(self, *args, **kwargs):
        # Resize images before saving
        if self.image1:
            self.image1 = resize_image_to_400x400(self.image1)
        if self.image2:
            self.image2 = resize_image_to_400x400(self.image2)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.part_name} ({self.brand} - {self.car_model})"
   
   


BID_STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Accepted", "Accepted"),
    ("Rejected", "Rejected"),
]

CONDITION_CHOICES = [
    ("Brand New", "Brand New"),
    ("Used", "Used"),
]


class Bid(models.Model):
    part_request = models.ForeignKey("orders.PartRequest", on_delete=models.CASCADE, related_name="bids")
    store = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default="Brand New")  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    image1 = models.ImageField(storage=MediaCloudinaryStorage(), upload_to="bid_images/", blank=True, null=True)
    image2 = models.ImageField(storage=MediaCloudinaryStorage(), upload_to="bid_images/", blank=True, null=True)
    status = models.CharField(max_length=10, choices=BID_STATUS_CHOICES, default="")    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Resize images before saving
        if self.image1:
            self.image1 = resize_image_to_400x400(self.image1)
        if self.image2:
            self.image2 = resize_image_to_400x400(self.image2)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bid by {self.store.username} for {self.part_request.part_name}"

    class Meta:
        ordering = ["status", "-price"]