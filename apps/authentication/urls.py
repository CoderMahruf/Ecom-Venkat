from django.urls import path 
from .views import SignupView,SigninView,SignoutView,RequestForgetPasswordView,VerifyOTPView,ForgetPasswordView

urlpatterns = [
    path('signup/',SignupView.as_view(),name='signup'),
    path('signin/',SigninView.as_view(),name='signin'),
    path('signout/',SignoutView.as_view(),name='signout'),


    

    # forget password 
    path('request-forget-password/', RequestForgetPasswordView.as_view(), name='request-forget-password'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('forget-password/', ForgetPasswordView.as_view(), name='forget-password'),
]
