from rest_framework import serializers
from .models import User, UserProfile
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            phone=validated_data.get('phone'),
            full_name=validated_data.get('full_name'),
            password=validated_data.get('password'),
        )
        UserProfile.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()  # email or phone
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        identifier = data.get('identifier')
        password = data.get('password')

        user = User.objects.filter(email=identifier).first() or User.objects.filter(phone=identifier).first()

        if user and user.check_password(password):
            data['user'] = user
            return data
        raise serializers.ValidationError("Invalid credentials")

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['nin', 'bvn', 'bank_account_number', 'bank_name']



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # not used here

    def validate(self, attrs):
        identifier = attrs.get("email")  # can be phone or email
        password = attrs.get("password")

        user = User.objects.filter(email=identifier).first() or User.objects.filter(phone=identifier).first()
        if user and user.check_password(password):
            data = super().get_token(user)
            return {
                'refresh': str(data),
                'access': str(data.access_token),
            }
        raise serializers.ValidationError("Invalid credentials")