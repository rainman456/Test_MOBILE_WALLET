from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


# Create your models here.
class CustomManager(BaseUserManager):
    def create_user(self, email, password,  **extra_fields):
        email = self.normalize_email(email)
        account = self.model( email=email, **extra_fields)
        account.set_password(password)
        account.save(using=self._db)

        return account 

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractUser):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    first_name = models.CharField(verbose_name='First Name', max_length=50)      
    last_name = models.CharField(verbose_name='Last Name', max_length=50)
    email = models.EmailField(verbose_name='Email Address', unique=True)
    country = CountryField(default='NG',blank=True, blank_label='Country')
    phone_number = PhoneNumberField(blank=True)
    username = None
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)




    objects=CustomManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    class Meta:
        ordering=['date_joined']

    
    def __str__(self):
        return self.first_name
"""
    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save()
"""
