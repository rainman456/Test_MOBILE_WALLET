from django.shortcuts import render
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction as transaction_decorators, utils
from rest_framework.views import APIView,View
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *
from users.models import UserProfile
from userwallets.models import WalletStats
from transactions.models import Transactions,Deposits,Transfers,Mobile_TopUp
import requests
import time
import json
#from thepeer import Thepeer
# Create your views here.



#view to make bank transfers
class BankTransferView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BankTransfer
    @swagger_auto_schema(request_body=BankTransfer)
    def post(self, request):
        with open('bankcodes.txt','r') as doc:
            codes={}
            for line in doc:
                lines = line.split()
                if lines:
                    codes.update({lines[0]:lines[1]})
        serializer = BankTransfer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                headers={"accept":"application/json",
                "content-type":"application/json","api-key":"giW6UPgKddYpfcYQgBaFnSn5kQVnt5R8"}
                gateway_url="https://sandboxapi.fincra.com/disbursements/payouts"
                user_id = serializer.validated_data['user_id']
                user=UserProfile.objects.get(id=user_id)
                email=user.email
                merch=serializer.save()
                business_id="64033e4d9fc454765ab40e84"
                bank_name= serializer.validated_data['bank_name']
                account_number= serializer.validated_data['bank_account_number']
                account_holder= serializer.validated_data['account_holder']
                first_name,last_name=account_holder.split()
                recp_amount= serializer.validated_data['amount']
                new_amount=float(rec_amount)
                transaction=Transactions.objects.select_related('account').get(id=user_id)
                owner=WalletStats.objects.select_related('account').get(id=rec_id)
                available_balance=owner.balance
                transfer_type= serializer.validated_data['transfer_type']
                currency= serializer.validated_data[' currency']
                bank_code=codes[bank_name]
                payload={ 
                    "business":business_id ,"sourceCurrency":currency ,
                    "destinationCurrency":currency,"amount":recp_amount,
                     "paymentDestination":"bank_account","customerReference":email ,"description":"Bank transfer",
                     "beneficiary":{
                        "firstName":first_name, "lastName":last_name,
                         "accountHolderName":account_holder,"accountNumber":account_number,
                         "type":"individual",   "bankCode":bank_code}
                        }
                payload_data=json.dumps(payload)
                transfer=Transfers.objects.create(
                    transfer_type=transaction_type,
                    amount=new_amount,
                    sender=user,
                    bank_account_number=account_number,
                    bank_name=bank_name,
                    recipient=account_holder)
                transfer.save()
                if available_balance >= new_amount:
                    max_retry=5
                    delay_retry=2
                    for retry in range(max_retry):
                        response=requests.post(gateway_url,json=payload_data,headers=headers)
                        print(response.json)
                        if response == 200:
                            return JsonResponse({'detail': 'Transfer successful.'}, status=200)
                            owner.balance-=new_amount
                            owner.save()
                            transaction.status='success'
                            transaction.save()
                        else:
                            return JsonResponse({'detail':'transfer errors'}, status=400)
                            transaction.status='failed'
                            transaction.save()
                            time.sleep(delay_retry)
                else:
                    return JsonResponse({'detail': 'insufficient funds.'}, status=400)
            except UserProfile.DoesNotExist or bank_name not in codes:
                return JsonResponse({'detail': 'Invalid user or bank.'}, status=400)
                

class WalletTransferView(APIView):
   permission_classes = [IsAuthenticated]
   serializer_class = WalletTransfer
   @swagger_auto_schema(request_body=WalletTransfer)
   def post(self, request):
       serializer = WalletTransfer(data=request.data)
       if serializer.is_valid(raise_exception=True):
        try:
            headers={"accept":"application/json","content-type":"application/json",
            "api-key":"giW6UPgKddYpfcYQgBaFnSn5kQVnt5R8"}
            gateway_url="https://sandboxapi.fincra.com/disbursements/payouts"
            user_id = serializer.validated_data['user_id']
            rec_id = serializer.validated_data['rec_id']
            transfer_type= serializer.validated_data['transfer_type']
            currency= serializer.validated_data[' currency']
            rec_amount= serializer.validated_data[' amount']
            new_amount=float(rec_amount)
            business_id="64033e4d9fc454765ab40e84"
            user=UserProfile.objects.get(id=user_id)
            recipient=UserProfile.objects.get(id=rec_id)
            bank_code="035"
            owner=WalletStats.objects.select_related('account').get(id=rec_id)
            account_number=owner.virtual_acn
            email=user.email
            transaction=Transactions.objects.select_related('account').get(id=user_id)
            first_name,last_name=recipient.split()
            payload={
                "business":business_id ,"sourceCurrency":currency ,
                "destinationCurrency":currency,"amount":rec_amount,
                "paymentDestination":"bank_account","customerReference":email ,
                "description":"Wallet transfer",
                "beneficiary":{
                    "firstName":first_name, "lastName":last_name, "accountHolderName":recipient,
                    "accountNumber":account_number, "type":"individual",  "bankCode":bank_code}}
            payload_data=json.dumps(payload)
            transfer=Transfers.objects.create(
                transfer_type=transaction_type,
                amount=new_amount,
                sender=user,
                bank_account_number=account_number,
                bank_name=bank_name,
                receiver=recipient)
            transfer.save()
            if available_balance >= new_amount:
                max_retry=5
                delay_retry=2
                for retry in range(max_retry):
                    print(response.json)
                    response=requests.post(gateway_url,json=payload_data,headers=headers)
                    if response == 200:
                        return JsonResponse({'detail': 'Transfer successful.'}, status=200)
                        owner.balance-=new_amount
                        owner.save()
                        transaction.status='success'
                        transaction.save()
                    else:
                        return JsonResponse({'detail':'transfer errors'}, status=400)
                        transaction.status='failed'
                        transaction.save()
                        time.sleep(delay_retry)
                else:
                    return JsonResponse({'detail': 'insufficient funds.'}, status=400)

        except UserProfile.DoesNotExist:
            return JsonResponse({'detail': 'Invalid user.'}, status=400)

"""
class EwalletTransferView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EWalletTransfer
    @swagger_auto_schema(request_body=EWalletTransferView)
    def post(self, request):
        serializer = WalletTransfer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
"""


class DepositsView(APIView):
    def update(self,ac_id,amount,name):
        transaction_type='wallet_deposit'
        wallet=get_object_or_404(WalletStats,wallet_id=ac_id)
        transaction=Transactions.objects.filter(account=wallet.owner)
        acn_number=user_account.virtual_acn
        bank_name="Wema Bank"
        owner.balance+=amount
        owner.save()
        deposits=Deposits.objects.create(
            deposit_type=transaction_type,
            amount=amount,creditor_name=name,
            bank_account_number=account_number,
            account=owner)
        deposits.save()
        transaction.status='success'
        transaction.save()



"""
class EWalletDepositView(APIView):
"""



class MobilePurchaseView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MobilePurchase
    @swagger_auto_schema(request_body=MobilePurchase)
    def post(self, request):
        serializer = MobilePurchase(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                headers={"accept":"application/json","content-type":"application/json",
                "api-key":"giW6UPgKddYpfcYQgBaFnSn5kQVnt5R8"}
                gateway_url="http://52.210.49.22:8001/api/v1/vend_airtime"
                user_id=serializer.validated_data['user_id']
                network_name=serializer.validated_data['network_name']
                phone_number=serializer.validated_data['phone_number']
                amount=serializer.validated_data['amount']
                user=UserProfile.objects.get(id=user_id)
                email=user.email
                new_amount=float(amount)
                transaction=Transfers.objects.select_related('account').get(id=user_id)
                owner=WalletStats.objects.select_related('account').get(id=user_id)
                payload={"amount":amount,"phone_no":phone_number,"telco":network_name,"reference":email}
                payload_data=json.dumps(payload)
                mobile=Mobile_TopUp.objects.create(
                    account= user,
                    amount = amount,
                    phone_number=phone_number,
                    network=network_name
                    )
                mobile.save()
                if available_balance >= new_amount:
                    max_retry=5
                    delay_retry=2
                    for retry in range(max_retry):
                        print(response.json)
                        response=requests.post(gateway_url,json=payload_data,headers=headers)
                        if response == 200:
                            return JsonResponse({'detail': 'mobile purchase successful.'}, status=200)
                            owner.balance-=new_amount
                            owner.save()
                            transaction.status='success'
                            transaction.save()
                        else:
                            return JsonResponse({'detail':'purchase errors'}, status=400)
                            transaction.status='failed'
                            transaction.save()
                            time.sleep(delay_retry)
                else:
                    return JsonResponse({'detail': 'insufficient funds.'}, status=400)


            except UserProfile.DoesNotExist:
                return JsonResponse({'detail': 'Invalid user.'}, status=400)











class Webhook(APIView):
    import hmac
    import hashlib
    import csv

    def post(self,request,*args,**kwargs):
        webhook_secret_key=''
        payload=request.data
        key = webhook_secret_key.encode('utf-8')
        message=json.dumps(payload,separators(',',':').encode('utf-8'))
        encrypted_data=hmac.new(key,message,hashlib.sha512).hexdigest()
        signature=request.headers.get('signature')
        if signature == encrypted_data:
            webhook_data=request.data
            event=webhook_data.get("event")
            if event == "collection.successful":
                virtual_id=webhook_data.get("virtualAccount")
                amount=float(webhook_data.get("amountReceived"))
                name=webhook_data.get("customerName")
                upate_view=DepositsView()
                update_view.update(virtual_id,amount,name)
                filename_3="webhook_Payins.csv"
                column_labels3=['Account id','Status','Payin Currency','Timestap']
                with open(filename_3,'a',newline='') as csvfile3:
                    csv_writer3=csv.DictWriter(csvfile3,fieldnames=column_labels3)
                    if csvfile3.tell==0:
                        csv_writer3.writeheader()
                    data_log3={
                        'Account id':webhook_data.get("virtualAccount"),'Status':webhook_data.get("status"),
                        'Payin Currency':webhook_data.get("destinationCurrency"),'Timestap':webhook_data.get("createdAt")}
                    csv_writer3.writerow(data_log3)
            if event == "payout.successful":
                filename2="webhook_Accounts.csv"
                column_labels=['Account','id','Status','Currency','Timestap']
                with open(filename2,'a',newline='') as csvfile:
                    csv_writer=csv.DictWriter(csvfile,fieldnames=column_labels)
                    if csvfile.tell==0:
                        csv_writer.writeheader()
                    data_log={
                        'Account':webhook_data.get("reference"),
                        'id':webhook_data.get("id"),
                        'Status':webhook_data.get("status"),
                        'Currency':webhook_data.get("sourceCurrency"),
                        'Timestap':webhook_data.get("createdAt")}
                    csv_writer.writerow(data_log)
            if event == "virtualaccount.approved":
                filename3="webhook_Accounts.csv"
                column_labels=['Account id','Status','Currency','Timestap']
                with open(filename3,'a',newline='') as csvfile:
                    csv_writer=csv.DictWriter(csvfile,fieldnames=column_labels)
                    if csvfile.tell==0:
                        csv_writer.writeheader()
                    data_log={
                        'Account id':webhook_data.get("id"),
                        'Status':webhook_data.get("status"),
                        'Currency':webhook_data.get("currency"),
                        'Timestap':webhook_data.get("createdAt")}
                    csv_writer.writerow(data_log)              
        else:
            return Response({'error':"invalid signature"},status=status.HTTP_400_BAD_REQUEST)



