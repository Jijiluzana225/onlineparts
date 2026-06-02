from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PartRequest
from django.utils import timezone
import requests

BOT_TOKEN = "8720277303:AAErCO6K-6boOYJFwYGQ70lyLXgZisQz0bU"
CHAT_ID = "-5115661768"


@receiver(post_save, sender=PartRequest)
def notify_new_request(sender, instance, created, **kwargs):

    if created:

        # Convert to Philippine time
        ph_time = timezone.localtime(instance.created_at)
        formatted_date = ph_time.strftime("%Y-%m-%d %H:%M:%S")

        # ✅ DEFINE FIRST (outside message)
        brand_new = "☑ Brand New" if instance.brand_new else "☐ Brand New"
        used = "☑ Used" if instance.used else "☐ Used"

        message = f"""
🚗 NEW PART REQUEST

Date: {formatted_date}
{brand_new}
{used}
Part: {instance.part_name}
Brand: {instance.brand}
Model: {instance.car_model}
Year: {instance.year}
Description: {instance.description}

Requested By: {instance.user.username}

https://www.getautoparts.shop/
"""

        try:
            requests.post(
                f"https://api.telegram.org/bot8720277303:AAErCO6K-6boOYJFwYGQ70lyLXgZisQz0bU/sendMessage",
                data={
                    "chat_id": -5115661768,
                    "text": message
                },
                timeout=10
            )
        except Exception as e:
            print("Telegram Error:", e)