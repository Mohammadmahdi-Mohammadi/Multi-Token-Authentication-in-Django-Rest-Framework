import json

from .models import Post
from account.models import User
from rest_framework import serializers
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title','text','is_enable','publish_date']

class RegisterSerializer(serializers.ModelSerializer):

  password = serializers.CharField(required=True, validators=[validate_password])
  password_Repeat = serializers.CharField(required=True)



  class Meta:
    model = User
    fields = ( 'username','password', 'password_Repeat','Phone')

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

  # def validate(self, data):
  #   Phone1 = data.get('Phone')
  #
  #   if  User.objects.filter(Phone=Phone1).exists():
  #     raise serializers.ValidationError({"Phone":"This number already exist"})
  #
  #   return data


  def create(self, validated_data):
    user = User.objects.create(
      username=validated_data['username'],
      Phone = validated_data['Phone']
      # Phone=validated_data['Phone']
      )
    user.set_password(validated_data['password'])
    user.save()
    return user









