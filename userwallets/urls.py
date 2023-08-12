from django.urls import include, path

from .views import *



urlpatterns = [
    # get the user's account number and account id endpoint
    path('api/v1/auth/getAccountNumbers/', GetVirtualAcnView.as_view(), name='get-AccountNumbers'),
    #get the user's account details endpoint
    path('api/v1/auth/getAccountDetails/user/<int:user_id>/', GetAccountDetailsView.as_view(), name='get-AccountDetails'),
    ]