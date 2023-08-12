from rest_framework import serializers
from .models import Transactions


class GetTransactionsDetails(serializers.ModelSerializer):
    class Meta:
        model=Transactions
        fields = [ 'account','transaction_type','transaction_id', 'amount', 'recipient','timestamp','status']