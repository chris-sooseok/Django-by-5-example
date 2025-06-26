

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Image

@receiver(post_save, sender=Image)
def clear_users_like(sender, instance, created, **kwargs):
    if created:
        instance.users_like.clear()  # This ensures it's empty right after creation