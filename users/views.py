from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from djoser import utils
from djoser.compat import get_user_email
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from djoser.views import UserViewSet,TokenDestroyView,TokenCreateView
from .serializers import CreateUser,OTPActivate,OTPResend,SendOTPPasswordReset,PasswordResetConfirm,LoginSerializer
from .models import UserProfile

import pyotp


global otp_secret,otp,otp_code 
otp_secret= pyotp.random_base32()
otp = pyotp.TOTP(otp_secret, digits=4)
otp_code=otp.now()
#@method_decorator(csrf_exempt,name='dispatch')
class CustomUserViewSet(UserViewSet):
    serializer_class=CreateUser
    def create(self, request, *args, **kwargs):
        serializer = CreateUser(data=request.data)
        print(serializer)
        print(request.data)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            if user:
                #send_mail('OTP Code',# Send OTP code via email
                #f'Your OTP code is: {otp_code}',settings.EMAIL_HOST_USER,
                #[serializer.validated_data['email']],fail_silently=False
                data={'detail': 'User created successfully. OTP code sent.',
                'email':user.email,'id':user.id}
                headers = self.get_success_headers(serializer.data)
                return JsonResponse(data, status=201, headers=headers)
        return JsonResponse(serializer.errors,status=400)

class ActivateView(APIView):        
    serializer_class=OTPActivate
    @swagger_auto_schema(request_body=OTPActivate)

    def post(self, request):
        serializer=OTPActivate(data=request.data)
        if serializer.is_valid(raise_exception=True):
            otp_c = serializer.validated_data['otp_code']
            user_id = serializer.validated_data['user_id']
            #request.session['otp_code']=otp_c
            print(otp_c)
            print(otp_code)
            print(request.session.get('otp'))
            try:
                user=UserProfile.objects.get(id=user_id)
            except UserProfile.DoesNotExist:
                return JsonResponse({'detail': 'Invalid user.'}, status=400)
            if  otp_c==otp_code:
                user=UserProfile.objects.get(id=user_id)
                user.is_active = True
                user.save()
                return JsonResponse({'detail': 'Account activated successfully.'},status=200)
            else:
                return JsonResponse({'detail': 'Invalid OTP code.'}, status=400)



class OTPResendView(APIView):
    serializer_class=OTPResend
    @swagger_auto_schema(request_body=OTPResend)

    def post(self, request):
        serializer=OTPResend(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user_id = serializer.validated_data['user_id']
                user=UserProfile.objects.get(id=user_id)
                email=user.email
                send_mail( 'OTP Code',f'Your OTP code is: {otp_code}',
                settings.EMAIL_HOST_USER,[email],
                fail_silently=False,)
            except UserProfile.DoesNotExist:
                return JsonResponse({'detail': 'Invalid user.'}, status=400)


class OTPResetEmailView(UserViewSet):
    serializer_class=SendOTPPasswordReset
    def reset_password(self, request, *args, **kwargs):
        serializer = SendOTPPasswordReset(data=request.data)
        serializer.is_valid(raise_exception=True)
        #self.reset_password(serializer)


        # Send OTP code via email
        send_mail(      
            'OTP Code',
            f'Your OTP code to reset your password is: {otp_code}',
            settings.EMAIL_HOST_USER,
            [serializer.validated_data['email']],
            fail_silently=False,
        )

        return JsonResponse({'detail': 'otp sent.'},status=200)


class ResetPasswordView(UserViewSet):
    serializer_class=PasswordResetConfirm
    def reset_password_confirm(self, request, *args, **kwargs):
        serializer = PasswordResetConfirm(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid=serializer.validated_data['uid']
        token=serializer.validated_data['token']
        new_password=serializer.validated_data['new_password']
        try:
            user=UserProfile.objects.get(id=uid)
        except UserProfile.DoesNotExist:
            return JsonResponse({'detail': 'Invalid user.'}, status=400)
        try:
            token_v=Token.objects.get(key=token,user=user)
        except Token.DoesNotExist:
            return JsonResponse({'detail': 'Invalid Token.'}, status=400)
        user.set_password(new_password)
        user.save()
        return JsonResponse({'detail': 'Password. changed '},status=200)

 
