import uuid
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .serializers import RegisterSerializer,UserSerializer  
from django.contrib.auth import get_user_model,authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from datetime import timedelta
from django.utils import timezone
from .utils import send_verification_email, send_password_reset_email
# Create your views here.
User=get_user_model()




class RegisterView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        email = request.data.get('email', '').strip()
        existing = User.objects.filter(email=email).first()
        if existing:
            if not existing.is_active:
                return Response(
                    {'error': 'This account has been deleted. Please contact support.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            if existing.is_blocked:
                return Response(
                    {'error': 'This account has been blocked. Please contact support.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            user.is_verified = False  
            user.verification_token = uuid.uuid4()
            user.save()
            send_verification_email(user)
            return Response(
                {"message": "Registered! Please check your email to verify your account."},
                status=status.HTTP_201_CREATED
            )
            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            user = User.objects.get(verification_token=token)
        except User.DoesNotExist:
            return Response({'error': 'Invalid or expired token'}, status=400)

        if user.is_verified:
            return Response({'message': 'Email already verified'})

        user.is_verified = True
        user.verification_token = None    # invalidate token after use
        user.save()
        return Response({'message': 'Email verified successfully! You can now log in.'})
    


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        
        email = request.data.get('email')
        password = request.data.get('password')

    
        if not email or not password:
            return Response(
                {'error': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_obj = User.objects.get(email=email)
            # print (User.objects.all())
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

      
        user = authenticate(
            request,
            username=user_obj.email,
            password=password
        )

        if not user:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        
        if not user.is_active:
            return Response(
                {'error': 'Your account has been deactivated'},
                status=status.HTTP_403_FORBIDDEN
            )
        if user.is_blocked:
            return Response(
                 {'error': 'Your account has been blocked. Please contact support.'},
                status=status.HTTP_403_FORBIDDEN

            )
        if not user.is_verified:
            return Response(
                {'error': 'Please verify your email before logging in.'},
                status=status.HTTP_403_FORBIDDEN
            )

       
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
    

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # ✅ don't reveal if email exists — security best practice
            return Response({'message': 'If this email exists, a reset link has been sent.'})

        user.reset_token = uuid.uuid4()
        user.reset_token_expiry = timezone.now() + timedelta(minutes=15)
        user.save()
        send_password_reset_email(user)
        return Response({'message': 'If this email exists, a reset link has been sent.'})

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token):
        new_password = request.data.get('password', '')
        confirm_password = request.data.get('confirm_password', '')

        if not new_password or len(new_password) < 6:
            return Response({'error': 'Password must be at least 6 characters'}, status=400)

        if new_password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=400)

        try:
            user = User.objects.get(reset_token=token)
        except User.DoesNotExist:
            return Response({'error': 'Invalid or expired reset link'}, status=400)

        # ✅ check expiry
        if user.reset_token_expiry and timezone.now() > user.reset_token_expiry:
            return Response({'error': 'Reset link has expired. Please request a new one.'}, status=400)

        user.set_password(new_password)
        user.reset_token = None
        user.reset_token_expiry = None
        user.save()
        return Response({'message': 'Password reset successfully! You can now log in.'})


class ResendVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'If this email exists, a verification link has been sent.'})

        if user.is_verified:
            return Response({'message': 'Email is already verified.'})

        user.verification_token = uuid.uuid4()
        user.save()
        send_verification_email(user)
        return Response({'message': 'Verification email resent!'})

    

class LogoutView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        refresh_token=request.data.get('refresh')

        if not refresh_token:
            return Response(
                {'error':'refresh token is required'},status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response({'Message':"Logged out successfully"},status=status.HTTP_200_OK)
        except:
            return Response({'message':"Invalid or expired token"},status=status.HTTP_400_BAD_REQUEST)





class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)