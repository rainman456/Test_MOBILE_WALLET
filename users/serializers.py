
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from djoser.serializers import (UserCreateSerializer,
  UserSerializer, ActivationSerializer,TokenCreateSerializer,SendEmailResetSerializer,
  PasswordResetConfirmSerializer)
from .models import UserProfile


class CreateUser(serializers.Serializer):
    class Meta:
        model = UserProfile
        fields = ["first_name", "last_name", "email", "password", "country", "phone_number"]


        

class UserCurrent(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = UserProfile
        fields = [ 'id','last_name', 'email', 'first_name', 'password', 'country', 'phone_number']


class LoginSerializer(TokenCreateSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)




class OTPActivate(serializers.Serializer):
    otp_code=serializers.CharField(max_length=4)
    user_id=serializers.IntegerField()


class OTPResend(serializers.Serializer):
    user_id=serializers.IntegerField()



class SendOTPPasswordReset(SendEmailResetSerializer):
    pass


class PasswordResetConfirm(serializers.Serializer):
    uid=serializers.IntegerField()
    token=serializers.CharField()
    new_password = serializers.CharField(required=True, write_only=True)






