from django.shortcuts import render
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction as transaction_decorators, utils
from rest_framework.views import APIView,View
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from users.models import UserProfile
from .models import WalletStats
from payments_app.views import Webhook
from rest_framework import status
import requests
import json
# Create your views here.
   

class GetVirtualAcnView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class =  GetVirtualAcn
    @swagger_auto_schema(request_body= GetVirtualAcn)
    def post(self, request):
        serializer =  GetVirtualAcn(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                #thepeer_instance=Thepeer('')
                user_id=serializers.validated_data['user_id']
                bvn=serializers.validated_data['bvn']
                user=UserProfile.objects.get(id=user_id)
                email=user.email
                #test=thepeer_instance.index_user(user,email,email)
                #peers_s=json.loads(test)
                date_of_birth=serializers.validated_data['d_o_b']
                first_name=serializers.validated_data['first_name']
                last_name=serializers.validated_data['last_name']
                bank_name=serializers.validated_data['bank_name']
                owner=WalletStats.objects.select_related('account').get(id=user_id)
                #peer_ref=peers_s["reference"]
                #owner.peer_ref=peer_ref
                #owner.save()
                headers={"accept":"application/json","content-type":"application/json",
                "api-key":"giW6UPgKddYpfcYQgBaFnSn5kQVnt5R8"}
                gateway_url="https://sandboxapi.fincra.com/profile/virtual-accounts/requests/"
                payload={"dateofBirth":date_of_birth,"accountType":'individual',"currency":currency,
                "KYCInformation":{"firstName":first_name, "lastName":last_name, "bvn":bvn},"channel":bank_name}
                payload_data=json.dumps(payload)
                responses=requests.post(gateway_url,json=payload_data,headers=headers)
               
                if responses.status_code == 200:
                    wdata=responses.data
                    stat=wdata.get('status')
                    wid=wdata.get('_id')
                    if stat == "approved":
                        virtualacn=webhook_data.get("accountNummber")
                        owner.virtual_acn=virtualacn
                        owner.wallet_id=wid
                        owner.save()
                    else:
                        return Response({'error':"unable to get account number"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error':"unable to get account number"},status=status.HTTP_400_BAD_REQUEST)
            except UserProfile.DoesNotExist:
                return JsonResponse({'detail': 'Invalid user '}, status=400)


class GetAccountDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    #serializer_class =  GetAccountDetails
    #@swagger_auto_schema(request_body= GetAccountDetails)
    def get(self, request,user_id):
            try:
                user=UserProfile.objects.get(id=user_id)
                owner=WalletStats.objects.select_related('account').get(id=user_id)
            except WalletStats.DoesNotExist:
                return JsonResponse({'detail': 'Invalid user or not found '}, status=404)
            serializer=GetAccountDetails(owner,many=True)
            response_data={
                'message':f'Account Details of {user}',
                'transactions':serializer.data}
            return JsonResponse(response_data,status=200)



