from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserSettings

@receiver(post_save, sender=User)
def create_settings(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_settings(sender, instance, **kwargs):
    instance.usersettings.save()