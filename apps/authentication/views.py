from rest_framework import status,generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer,SigninSerializer,ChangePasswordSerializer
from .models import UserOtp
from django.contrib.auth import get_user_model
import random
from django.core.mail import send_mail
from django.conf import settings
from uuid import uuid4
from django.utils import timezone
from datetime import timedelta
User = get_user_model()
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
# from .utils import activation_token_generator
# Create your views here.

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "user": serializer.data,
                "message": "User created successfully",
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # for email verification view
# class SignupView(generics.CreateAPIView):
#     serializer_class = SignupSerializer
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save(is_active=False)
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         # token = activation_token_generator.make_token(user)
#         token = default_token_generator.make_token(user)
#         link = f"http://127.0.0.1:8000/api/activate/{uid}/{token}/"
#         send_mail(
#             subject="Activate your account",
#             message=f"Click to activate your account: {link}",
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[user.email],
#         )
#         return Response({'message': 'Check your email for the activation link.'}, status=status.HTTP_201_CREATED)
    
# class EmailActivateAccountView(APIView):
#     def get(self, request, uidb64, token):
#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             return Response({'error': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)
#         if user.is_active:
#             return Response({'message': 'Account already activated.'})
#         # if activation_token_generator.check_token(user, token):
#         if default_token_generator.check_token(user, token):
#             user.is_active = True
#             user.save()
#             return Response({'message': 'Account activated successfully!'})
#         return Response({'error': 'Activation link expired or invalid.'}, status=status.HTTP_400_BAD_REQUEST)


class SigninView(APIView):
    def post(self, request):
        serializer = SigninSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "message":"Login Successfully",
            "user": {
                "id": user.id,
                "Full Name": f"{user.first_name} {user.last_name}",
            }
        })

class SignoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class RequestForgetPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Email not found."}, status=404)
        
        otp = random.randint(100000, 999999)
        token = uuid4()
        user_otp = UserOtp.objects.create(otp=otp, token=token,user=user)
        
        send_mail(
            subject="Your Password Reset OTP",
            message=f"Your OTP is {otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],

        )
        return Response({
            "message": "OTP sent to your email.",
            "token": token,
        })
    
class VerifyOTPView(APIView):
    def post(self, request):
        otp = request.data.get("otp")
        token = request.data.get("token")
        if not all([otp, token]):
            return Response({"error": "OTP and token are required."}, status=400)

        match = UserOtp.objects.filter(token=token, otp=otp).select_related('user').first()
        if match:
            expiry_time = match.created_at + timedelta(minutes=1)
            if timezone.now() > expiry_time:
                return Response({"error": "OTP has expired."}, status=400)
            
            return Response({
                "message": "OTP verified.",
                "token": match.token 
            }, status=200)
        else:
            return Response({"error": "Invalid OTP."}, status=400)

class ForgetPasswordView(APIView):
    def post(self, request):
        password = request.data.get("password")
        token = request.data.get("token")
        if not password:
            return Response({"error": " password are required."}, status=400)

        try:
            user = UserOtp.objects.get(token=token).user
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        user.set_password(password)
        user.save()

        return Response({"message": "Password set successfully."}, status=200)

