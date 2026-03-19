from django.shortcuts import render
from .serializers import RegisterSerializer,UserSerializer,LoginSerializer
from django.contrib.auth import get_user_model,authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
# Create your views here.
User=get_user_model()

class RegisterView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response({"message":"Register Successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


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

       
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
    

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