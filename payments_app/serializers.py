from rest_framework import serializers



class BankTransfer(serializers.Serializer):
    user_id = serializers.IntegerField()
    transfer_type=serializers.CharField()
    bank_name=serializers.CharField()
    bank_account_number=serializers.CharField()
    account_holder=serializers.CharField()
    amount=serializers.CharField()
    currency=serializers.CharField()




class WalletTransfer(serializers.Serializer):
    user_id= serializers.IntegerField()
    rec_id=serializers.IntegerField()
    currency=serializers.CharField()
    transfer_type=serializers.CharField()
    amount=serializers.CharField()


"""
class EwalletTransfer(serializers.Serializer):
    user_id= serializers.IntegerField()
    ewallet_name=serializers.CharField()
    currency=serializers.CharField()
    amount=serializers.DecimalField()
   


class CardDeposit(serializers.Serializer):
    user_id=serializers.IntegerField()



class EWalletDeposit(serializers.Serializer):
    user_id=serializers.IntegerField()
"""

class MobilePurchase(serializers.Serializer):
    transaction_type=serializers.CharField()
    user_id=serializers.IntegerField()
    network_name=serializers.CharField()
    phone_number=serializers.CharField()
    amount=serializers.IntegerField()


