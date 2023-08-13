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
from transactions.models import Transactions,Deposits,Transfers,Mobile_TopUp
import requests
import json
# Create your views here.

class GetTransactionsDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    #serializer_class=GetTransactionsDetails
    #@swagger_auto_schema(request_body= GetTransactionsDetails)
    def get(self, request,user_id):
            try:
                user=UserProfile.objects.get(id=user_id)
                transaction=owner=Transactions.objects.get(account=user)
            except Transactions.DoesNotExist:
                return JsonResponse({'detail': 'Invalid user or not found '}, status=404)
            serializer=GetTransactionsDetails(transaction,many=true)
            response_data={
                'message':f'Transactions for {user}',
                'transactions':serializer.data
            }
            return JsonResponse(response_data)
