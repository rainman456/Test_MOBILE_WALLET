from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from .models import UserProfile
from userwallets.models import WalletStats

@receiver(post_save, sender=UserProfile)
def create_wallet(sender, created, instance, *args, **kwargs):
    if created:
        WalletStats.objects.create(owner=instance)


@receiver(post_save, sender=User)
def create_wallet(sender, created, instance, *args, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

