import json

from rest_framework import serializers
from account.models import User
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Post
# from .models import User
# from . import views
# from phonenumber_field.modelfields import PhoneNumberField
# from .models import ExtendedUserExample




class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title','text','is_enable','publish_date']




class RegisterSerializer(serializers.ModelSerializer):
  # email = serializers.EmailField(
  #   required=True,
  #  validators=[UniqueValidator(queryset=User.objects.all())]
  # )
  password = serializers.CharField(required=True, validators=[validate_password])
  password_Repeat = serializers.CharField(required=True)
  # email123 = serializers.EmailField(source="user.email")
  # phone = serializers.CharField(source="user.password")
  # # pass1 = serializers.PKOnlyObject()

  # Phone = serializers.CharField(required=True, validators=)
  # Phone = serializers.CharField(required=True)
  # phone_num = serializers.CharField(required=True)
  # phone_number = PhoneNumberField(unique=True, null=False, blank=False)
  # name = serializers.CharField()



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



  def create(self, validated_data):
    user = User.objects.create(
      username=validated_data['username'],
      # Phone=validated_data['Phone']
      )
    user.set_password(validated_data['password'])
    user.save()
    return user







