from django.urls import include, path
from djoser.urls import authtoken
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet,ActivateView,
OTPResendView,OTPResetEmailView,ResetPasswordView)



urlpatterns = [
    # User creation endpoint
    path('api/v1/auth/users/create/', CustomUserViewSet.as_view({'post': 'create'}), name='user-create'),
    # OTP verification endpoint
    path('api/v1/auth/users/activate/', ActivateView.as_view(), name='user-activate'),
     # OTP resend endpoint
    path('api/v1/auth/users/otp-resend/', OTPResendView.as_view(), name='otp-resend'),
    
    path('api/v1/auth/users/reset_password/', OTPResetEmailView.as_view({'post': 'reset_password'}), name='reset-password'),

    path('api/v1/auth/users/reset_password_confirm/', ResetPasswordView.as_view({'post': 'reset_password_confirm'}), name='reset-password-vc'),

    # Token authentication endpoint (optional)
    #path('auth/', include(authtoken)),
    # Other URLs...
]
