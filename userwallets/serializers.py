from rest_framework import serializers
from .models import WalletStats

class GetVirtualAcn(serializers.Serializer):
    user_id=serializers.CharField()
    bvn=serializers.CharField()
    d_o_b=serializers.DateTimeField(format='%d/%m/%y')
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    bank_name=serializers.CharField()
class GetAccountDetails(serializers.ModelSerializer):
    class Meta:
        model=WalletStats
        fields = [ 'owner','balance', 'currency', 'virtual_acn','wallet_id','created_at']

 