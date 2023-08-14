from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
import binascii
from users.models import UserProfile
import random 
import os 
from django.utils import timezone
from PIL import Image
#Create your models here.



class WalletStats(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    wallet_id = models.CharField(max_length=50)
    is_disabled = models.BooleanField(default=False)
    #peer_ref=models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency= models.CharField(max_length=6)
    virtual_acn=models.CharField(max_length=20)
    created_at=models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name_plural="User Wallets"
    def __str__(self):
        return self.owner.email
"""
class Profile(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='media/')
    house_address= models.CharField(max_length=255)
    img = Image.open(self.profile_pic.path)
    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(self.image.path)
    super().save(*args, **kwargs)
    class Meta:
        verbose_name_plural="User Profiles"
    def __str__(self):
        return self.owner.email
"""
