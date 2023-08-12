from django.contrib import admin
from .models import Transactions,Deposits,Transfers,Mobile_TopUp

@admin.register(Deposits)
class DepositsAdmin(admin.ModelAdmin):
    list_display=('account','deposit_type','amount',)
    search_fields=['account']
   
@admin.register(Transfers)
class TransfersAdmin(admin.ModelAdmin):
    list_display=('sender','transfer_type','amount','receiver','recipient',)
    search_fields=['sender','receiver','recipient']
   
@admin.register(Mobile_TopUp)
class MobileAdmin(admin.ModelAdmin):
    list_display=('account','amount',)
    search_fields=['account']
   
@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display=('account','transaction_type','transaction_id','amount','timestamp','recipient' ,'status',)
    list_filter=['timestamp','status','transaction_type']
    search_fields=['account']
   