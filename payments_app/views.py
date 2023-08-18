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
from transactions.signals import create_transfer
import requests
import time
import json
import os
import hmac
import hashlib
import csv
#from thepeer import Thepeer
# Create your views here.



#view to make bank transfers
class BankTransferView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BankTransfer
    @swagger_auto_schema(request_body=BankTransfer)
    def post(self, request):
        BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path=os.path.join(BASE_DIR,'bankcodes.txt')
        with open(file_path,'r') as doc:
            codes={}
            for line in doc:
                lines = line.split()
                if lines:
                    codes.update({lines[1]:lines[0]})
        serializer = BankTransfer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                headers={"accept":"application/json",
                "content-type":"application/json","api-key":"9k8NHNDPPEzCNxECBBE26XVF85jsv8tx"}
                gateway_url="https://sandboxapi.fincra.com/disbursements/payouts"
                user_id = serializer.validated_data['user_id']
                user=UserProfile.objects.get(id=user_id)
                email=user.email
                business_id="64033e4d9fc454765ab40e84"
                bank_name= serializer.validated_data['bank_name']
                account_number= serializer.validated_data['bank_account_number']
                account_holder= serializer.validated_data['account_holder']
                first_name,last_name=account_holder.split()
                recp_amount= serializer.validated_data['amount']
                new_amount=float(recp_amount)
                #transaction=Transactions.objects.get(account=user)
                owner=WalletStats.objects.get(owner=user)
                available_balance=owner.balance
                transfer_type='bank_transfer'
                currency= serializer.validated_data['currency']
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
                transfer=Transfers.objects.create(
                    transfer_type=transfer_type,
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
                        response=requests.post(gateway_url,json=payload,headers=headers)
                        print(response.json())
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
                    transaction.status='failed'
                    transaction.save()
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
            "api-key":"9k8NHNDPPEzCNxECBBE26XVF85jsv8tx"}
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
            owner2=WalletStats.objects.get(owner=recipient)
            owner1=WalletStats.objects.get(owner=user)
            account_number=owner.virtual_acn
            email=user.email
            transaction=Transactions.objects.get(account=user)
            transaction2=Transactions.objects.get(account=recipient)
            first_name,last_name=recipient.split()
            payload={
                "business":business_id ,"sourceCurrency":currency ,
                "destinationCurrency":currency,"amount":rec_amount,
                "paymentDestination":"bank_account","customerReference":email ,
                "description":"Wallet transfer",
                "beneficiary":{
                    "firstName":first_name, "lastName":last_name, "accountHolderName":recipient,
                    "accountNumber":account_number, "type":"individual",  "bankCode":bank_code}}
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
                    print(response.json())
                    response=requests.post(gateway_url,json=payload_data,headers=headers)
                    if response == 200:
                        return JsonResponse({'detail': 'Transfer successful.'}, status=200)
                        owner1.balance-=new_amount
                        owner2.balance+=new_amount
                        owner1.save()
                        owner2.save()
                        transaction.status='success'
                        transaction2.status='success'
                        transaction.save()
                        transaction2.save()
                    else:
                        return JsonResponse({'detail':'transfer errors'}, status=400)
                        transaction.status='failed'
                        transaction2.status='failed'
                        transaction.save()
                        transaction2.save()
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
                "api-key":"9k8NHNDPPEzCNxECBBE26XVF85jsv8tx"}
                gateway_url="http://52.210.49.22:8001/api/v1/vend_airtime"
                user_id=serializer.validated_data['user_id']
                network_name=serializer.validated_data['network_name']
                phone_number=serializer.validated_data['phone_number']
                amount=serializer.validated_data['amount']
                user=UserProfile.objects.get(id=user_id)
                email=user.email
                new_amount=float(amount)
                transaction=Transactions.objects.get(account=user)
                owner=WalletStats.objects.get(owner=user)
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
    def process_webhook(self,payload,signature):
        webhook_secret_key='90c02a4ae9a34a938d87f2dda3ec5da8'
        payload=request.data
        key = webhook_secret_key.encode('utf-8')
        message=json.dumps(payload,separators=(',',':')).encode("utf-8")
        encrypted_data=hmac.new(key,message,hashlib.sha512).hexdigest()
        signature=request.headers['signature']
        if signature == encrypted_data:
            print("Processing data:" , payload )
            webhook_data=request.data
            current=json.loads(webhook_data)
            event=current["event"]
            if event == "collection.successful":
                virtual_id= current["data"]["virtualAccount"]
                amount=float(current["data"]["amountReceived"])
                name=current["data"]["customerName"]
                owner=WalletStats.objects.get(wallet_id=virtual_id)
                transaction_type='wallet_deposit'
                account_number=owner.virtual_acn
                bank_name="Wema Bank"
                owner.balance+=amount
                owner.save()
                deposits=Deposits.objects.create(
                    deposit_type=transaction_type,
                    amount=amount,creditor_name=name,
                    bank_account_number=account_number,
                    account=owner)
                deposits.save()    
                filename_3="webhook_Payins.csv"
                column_labels3=['Account id','Status','Payin Currency','Timestap']
                with open(filename_3,'a',newline='') as csvfile3:
                    csv_writer3=csv.DictWriter(csvfile3,fieldnames=column_labels3)
                    if csvfile3.tell==0:
                        csv_writer3.writeheader()
                    data_log3={
                        'Account id':virtual_id,
                        'Status':current["data"]["status"],
                        'Payin Currency': current["data"]["destinationCurrency"],
                        'Timestap':current["data"]["createdAt"]}
                    csv_writer3.writerow(data_log3)
            if event == "payout.successful":
                filename2="webhook_Accounts.csv"
                column_labels=['Account','id','Status','Currency','Timestap']
                with open(filename2,'a',newline='') as csvfile:
                    csv_writer=csv.DictWriter(csvfile,fieldnames=column_labels)
                    if csvfile.tell==0:
                        csv_writer.writeheader()
                    data_log={
                        'Account':current["data"]["reference"],
                        'id':current["data"]["id"],
                        'Status':current["data"]["status"],
                        'Currency': current["data"]["sourceCurrency"],
                        'Timestap':current["data"]["createdAt"]}
                    csv_writer.writerow(data_log)
            if event == "virtualaccount.approved":
                filename3="webhook_Accounts.csv"
                column_labels=['Account id','Status','Currency','Timestap']
                with open(filename3,'a',newline='') as csvfile:
                    csv_writer=csv.DictWriter(csvfile,fieldnames=column_labels)
                    if csvfile.tell==0:
                        csv_writer.writeheader()
                    data_log={
                        'Account id':current["data"]["id"],
                        'Status':current["data"]["status"],
                        'Currency':current["data"]["currency"],
                        'Timestap':current["data"]["createdAt"]}
                    csv_writer.writerow(data_log)
            return JsonResponse({'message': 'webhook processed.'}, status=200)
        else:
            print("Processing data:" , payload )
            return Response({'error':"invalid signature"},status=status.HTTP_400_BAD_REQUEST)
    def post(self,request):
        payload=request.data
        signature=request.headers.get('signature')
    def get(self,request):
        payload=request.data
        signature=request.headers.get('signature')
        return self.process_webhook(payload,signature)
            
