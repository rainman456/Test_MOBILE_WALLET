from django.urls import include, path

from .views import *



urlpatterns = [
    # Bank transfer endpoint
    path('api/v1/auth/bank_transfer/', BankTransferView.as_view(), name='bank-transfer'),
    # Vail wallet transfer endpoint
    path('api/v1/auth/wallet_transfer/', WalletTransferView.as_view(), name='user-activate'),
     # Mobile purchase endpoint
    path('api/v1/auth/mobile_purchase/', MobilePurchaseView.as_view(), name='airtime-purchase'),
    # webhook url
    path('api/v1/vail/webhook/', Webhook.as_view(), name='webhook'),
   
]