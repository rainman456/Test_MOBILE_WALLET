from django.contrib import admin
from .models import *

@admin.register(WalletStats)
class WalletssAdmin(admin.ModelAdmin):
    list_display=('owner','wallet_id','is_disabled','balance','currency','virtual_acn','created_at',)
    search_fields=['owner']
   

