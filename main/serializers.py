from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserInfo


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data.get('email')
        user = User.objects.create_user(username=username, password=password, email=email)
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserInfo
        fields = ('user', 'container_name', 'subscription_type', 'storage_quota_bytes', 'storage_used_bytes', 'dob', 'email_id')


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    email_id = serializers.EmailField(required=False, allow_blank=True)

    def validate(self, data):
        if data.get('password1') != data.get('password2'):
            raise serializers.ValidationError('Passwords do not match')
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
