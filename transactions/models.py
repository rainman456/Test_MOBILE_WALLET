from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
import string
from users.models import UserProfile
from userwallets.models import WalletStats
import random 
import os 
from django.utils import timezone

# Create your models here.


def generate_transaction_id():
    chars=string.ascii_uppercase + string.digits
    tid = "#"+''.join(random.choices(chars,k=12))
    return tid

    #  fields common to all payments

class Deposits(models.Model):
        #  fields common to all Deposits
    types=(('wallet_deposit','Wallet Deposit'),)
    deposit_type= models.CharField(choices=types,max_length=50)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    account = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    creditor_name = models.CharField(max_length=50)
    class Meta:
        verbose_name_plural="Deposits"
    def __str__(self):
        return self.account.email
   
class Transfers(models.Model):
        #  fields common to all Transfers
    types=(('bank_transfer','Bank Transfer'),
    ('wallet_transfer','Wallet Transfer'),('ewallet_transfer','eWallet Transfer'),)
    transfer_type= models.CharField(choices=types,max_length=50)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    sender = models.ForeignKey(UserProfile ,related_name='sender',on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile,related_name='receiver', on_delete=models.CASCADE,null=True)
    recipient =  models.CharField(max_length=50,default='x')
    bank_account_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=50)
    class Meta:
        verbose_name_plural="Transfers"
    def __str__(self):
        return self.account.email

class Mobile_TopUp(models.Model):
    account = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    phone_number=models.CharField(max_length=11)
    network = models.CharField(max_length=10)
    class Meta:
        verbose_name_plural="Mobile Transactions"
    def __str__(self):
        return self.account.email   

class Transactions(models.Model):
    STATUS=(('success','Successful'),('errors','failed'),('processing','Processing'),)
    TYPES=(('wallet_deposit','Wallet Deposit'),('bank_transfer','Bank Transfer')
    ,('wallet_transfer','Wallet Transfer'),('mobile_purchase','Mobile Purchase'),)
    account = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    transaction_type = models.CharField(choices=TYPES,max_length=50)
    transaction_id = models.CharField(max_length=13, validators=[MinLengthValidator(13),
    MaxLengthValidator(13)], default=generate_transaction_id)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp =  models.DateTimeField(default=timezone.now)
    recipient= models.CharField(max_length=60)
    status = models.CharField(choices=STATUS,max_length=50)
    class Meta:
        verbose_name_plural="All Transactions"
    def update_status(self, new_status):        
        self.status = new_status
        self.save()
    def __str__(self):
        return self.account.email   
