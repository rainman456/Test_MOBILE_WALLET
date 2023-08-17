from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from .models import Transactions,Deposits,Transfers,Mobile_TopUp

@receiver(post_save, sender=Deposits)
def create_deposit(sender, created, instance, *args, **kwargs):
    if created:
        deposit_type='wallet_deposit'
        Transactions.objects.create(
            transaction_type=deposit_type,
            account=instance.account,
            amount=instance.amount,
            recipient=instance.account)



@receiver(post_save, sender=Transfers)
def create_transfer(sender, created, instance, *args, **kwargs):
    if created:
        if instance.transfer_type=='bank_transfer':
           transaction=Transactions.objects.create(
                transaction_type=instance.transfer_type,
                account=instance.sender,
                amount=instance.amount,
                recipient=instance.recipient)
            return transaction
        elif instance.transfer_type=='wallet_transfer':
           transaction=Transactions.objects.create(
                transaction_type=instance.transfer_type,
                account=instance.sender,
                amount=instance.amount,
                recipient=instance.receiver)
            return transaction



@receiver(post_save, sender=Mobile_TopUp)
def create_mobile(sender, created, instance, *args, **kwargs):
    if created:
        transaction_type='mobile_purchase'
        Transactions.objects.create(
            transaction_type=transaction_type,
            account=instance.account,
            amount=instance.amount,
            recipient=instance.phone_number)
