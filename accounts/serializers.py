from rest_framework import serializers
from django.contrib.auth import get_user_model

User=get_user_model()

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=['id','username','email','is_admin','phone','address']

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,min_length=6)
    confirmpassword=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['username','email','password','confirmpassword']

    def validate_email(self,value): 
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError('Email already exists')
            return value
    
    def validate_password(self,value):
         if len(value)<6:
              raise serializers.ValidationError('Password too short')
         if value.isdigit():
              raise serializers.ValidationError('password cannot be numbers')
         return value
    
    def validate_username(self,value):
         if User.objects.filter(username=value).exists():
              raise serializers.ValidationError('Username already taken')
         return value
    
    def validate(self,data):
         if data['password'] != data['confirmpassword']:
              raise serializers.ValidationError({
                   'confirmpassword':'passwords do not match'
              })
         return  data
            
            
    def create(self,validated_data):
            validated_data.pop('confirmpassword')
            user=User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            return user


class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)