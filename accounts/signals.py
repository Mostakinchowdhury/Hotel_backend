from accounts.models import CustomUser
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from threading import Thread
from django.conf import settings

from .models import *

User = get_user_model()



@receiver(post_save, sender=CustomUser)
def send_welcome_email_to_user(sender, instance, created, **kwargs):
    Profile.objects.get_or_create(user=instance)
    if created:
       print(f"user created username: {instance.username} email: {instance.email} at {instance.created_at}")
    else:
       print(f"user updated username: {instance.username} email: {instance.email} at {instance.updated_at}")
    
