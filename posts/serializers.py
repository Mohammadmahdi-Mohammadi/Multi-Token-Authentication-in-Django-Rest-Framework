

from django.contrib.auth import authenticate
from rest_framework.exceptions import NotFound

from .models import Post
from account.models import User
from rest_framework import serializers, exceptions
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import MultiTokens


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'is_enable', 'publish_date']




def Provider_check(data):
    print("+++++++++++++++++++++++++++++++")
    print("Provider_Check is done")
    print("+++++++++++++++++++++++++++++++")

    check_phone = data['Phone']
    MCI = check_phone.startswith(('990','991','992','993','994','911','912','913','914','915','916','917','918'),3)
    MTN_Irancell = check_phone.startswith(('930','933','935','936','937','938','939','901','902','903','904','905','941'),3)
    Rightel = check_phone.startswith(('920','921','922'),3)
    Talia = check_phone.startswith(('932'),3)
    Espadan = check_phone.startswith(('931'),3)
    Kish = check_phone.startswith(('934'),3)
    Students = check_phone.startswith(('994'),3)
    Shatel_virtual =check_phone.startswith(('998'),3)

    if MCI:
        return 'MCI'
    elif MTN_Irancell:
        return 'MTN-Irancell'
    elif Rightel:
        return 'Rightel'
    elif Talia:
        return 'Talia'
    elif Espadan:
        return 'Espadan'
    elif Kish:
        return 'Kish'
    elif Students:
        return 'Students'
    elif Shatel_virtual:
        return 'Shatel-Virtual'
    else:
        return 'not recognized'

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
            Phone=validated_data['Phone'],
            provider=Provider_check(validated_data)
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


class ListTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiTokens
        fields = ['id', 'name']


class KillTokenSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(), required=True, allow_null=False, min_length=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tokens = None

    def validate_ids(self, value):
        tokens = MultiTokens.objects.filter(id__in=value)
        if len(tokens) != len(value):
            raise NotFound()
        self._tokens = tokens
        return value

    @property
    def validated_data(self):
        _validated_data = super().validated_data
        _validated_data['tokens'] = self._tokens
        return _validated_data




