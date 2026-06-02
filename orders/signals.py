from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PartRequest
import requests

BOT_TOKEN = "8720277303:AAErCO6K-6boOYJFwYGQ70lyLXgZisQz0bU"
CHAT_ID = "8970132440"


@receiver(post_save, sender=PartRequest)
def notify_new_request(sender, instance, created, **kwargs):

    if created:

        message = f"""
🚗 NEW PART REQUEST

Date: {instance.created_at.strftime('%Y-%m-%d %H:%M:%S')}
Part: {instance.part_name}
Brand: {instance.brand}
Model: {instance.car_model}
Year: {instance.year}
Description: {instance.description}

Requested By:
{instance.user.username}

https://www.getautoparts.shop/

"""

        try:
            requests.post(
                f"https://api.telegram.org/bot8720277303:AAErCO6K-6boOYJFwYGQ70lyLXgZisQz0bU/sendMessage",
                data={
                    "chat_id": 8970132440,
                    "text": message
                },
                timeout=10
            )
        except Exception as e:
            print("Telegram Error:", e)