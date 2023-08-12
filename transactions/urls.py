from django.urls import include, path

from .views import *



urlpatterns = [
    #  Transactions endpoint
    path('api/v1/auth/user_transactions/user/<int:user_id>/', GetTransactionsDetailsView.as_view(), name='get-transactions'),
    ]