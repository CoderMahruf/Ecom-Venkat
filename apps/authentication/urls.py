from django.urls import path 
from .views import SignupView
# for email activation 
# from .views import EmailActivateAccountView
from .views import SigninView,SignoutView,ChangePasswordView,RequestForgetPasswordView,VerifyOTPView,ForgetPasswordView

urlpatterns = [
    path('signup/',SignupView.as_view(),name='signup'),

    # # for email activation 
    # path('signup/',SignupView.as_view(),name='signup'),
    # path('activate/<uidb64>/<token>/', EmailActivateAccountView.as_view(), name='activate'),

    path('signin/',SigninView.as_view(),name='signin'),
    path('signout/',SignoutView.as_view(),name='signout'),

    # change password
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    # forget password 
    path('request-forget-password/', RequestForgetPasswordView.as_view(), name='request-forget-password'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('forget-password/', ForgetPasswordView.as_view(), name='forget-password'),
]
