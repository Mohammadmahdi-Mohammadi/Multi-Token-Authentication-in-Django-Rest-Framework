import json

from django.contrib.auth import authenticate

from .models import Post
from account.models import User
from rest_framework import serializers, exceptions
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'is_enable', 'publish_date']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, validators=[validate_password])
    password_Repeat = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_Repeat', 'Phone')

        extra_kwargs = {
            # 'password': {'write_only': True},
            # 'Phone': {'validators': []}
            # 'phone': {'validators': [UniqueValidator(queryset=User.objects.all())]}
        }

    def validate(self, data):
        if data['password'] != data['password_Repeat']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            Phone=validated_data['Phone']
            # Phone=validated_data['Phone']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class loginserializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                data['user'] = user
            else:
                raise exceptions.ValidationError("Unable to login, wrong pass or username may cause it! ")
        else:
            raise exceptions.ValidationError("please Enter Username and password both!")
        return data


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_pass_repeat = serializers.CharField(required=True)



class ForgetPasswordSerializer(serializers.Serializer):
    model = User
    username = serializers.CharField(required=True)
    OTP = serializers.IntegerField(required=True)
    new_password = serializers.CharField(required=True)
    new_pass_repeat = serializers.CharField(required=True)

