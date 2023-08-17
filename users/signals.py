from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from .models import UserProfile
from userwallets.models import WalletStats
from transactions.models import *

"""
@receiver(post_save, sender=UserProfile)
def create_user(sender, created, instance, *args, **kwargs):
    if created:
        Transactions.objects.create(account=instance)
"""


@receiver(post_save, sender=UserProfile)
def create_wallet(sender, created, instance, *args, **kwargs):
    if created:
        WalletStats.objects.create(owner=instance)


