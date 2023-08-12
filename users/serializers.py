
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from djoser.serializers import (UserCreateSerializer,
  UserSerializer, ActivationSerializer,TokenCreateSerializer,SendEmailResetSerializer,
  PasswordResetConfirmSerializer)
from .models import UserProfile


class CreateUser(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = UserProfile
<<<<<<< HEAD
        fields = ["last_name", "email", "first_name", "password", "country", "phone_number"]
=======
        fields = ['last_name', 'email', 'first_name', 'password', 'country', 'phone_number']
>>>>>>> 663b1ddadf92585f133e2ce04633ed7ec4960a80

        

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






