


from .models import MultiTokens
from .models import Post
from account.models import User

from rest_framework import serializers,exceptions
from rest_framework.exceptions import NotFound

# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'is_enable', 'publish_date']

# def Provider_check(data):
#     # print("+++++++++++++++++++++++++++++++")
#     # print("Provider_Check is done")
#     # print("+++++++++++++++++++++++++++++++")
#
#     check_phone = data['Phone']
#
#     MCI = check_phone.startswith(('990','991','992','993','994','911','912','913','914','915','916','917','918'),3)
#     MTN_Irancell = check_phone.startswith(('930','933','935','936','937','938','939','901','902','903','904','905','941'),3)
#     Rightel = check_phone.startswith(('920','921','922'),3)
#     Talia = check_phone.startswith(('932'),3)
#     Espadan = check_phone.startswith(('931'),3)
#     Kish = check_phone.startswith(('934'),3)
#     Students = check_phone.startswith(('994'),3)
#     Shatel_virtual = check_phone.startswith(('998'),3)
#
#     if MCI:
#         return 'MCI'
#     elif MTN_Irancell:
#         return 'MTN-Irancell'
#     elif Rightel:
#         return 'Rightel'
#     elif Talia:
#         return 'Talia'
#     elif Espadan:
#         return 'Espadan'
#     elif Kish:
#         return 'Kish'
#     elif Students:
#         return 'Students'
#     elif Shatel_virtual:
#         return 'Shatel-Virtual'
#     else:
#         return 'not recognized'


class ThisIsInsane(object):
    def call_everything(self):
        # count = 0
        for name in dir(self):
            obj = getattr(self, name)
            # print("count is: ", count)
            # count += 1
            if callable(obj) and name != 'call_everything' and name[:2] != '__':
                bool, provider = obj()
                if bool == True:
                    print("*******************")
                    bool , provider = obj()
                    print("num is:", provider)
                    print("*******************")
                    return provider





class provider_check(ThisIsInsane):

    def __init__(self,phone):
        self.phone = phone

    def MCI(self):

        MCI = self.phone.startswith(
            ('990', '991', '992', '993', '994', '911', '912', '913', '914', '915', '916', '917', '918'), 3)
        # print("MCI is: ", MCI)
        # print("Phone is: ", self.phone)

        if MCI:
            return True, "MCI"
        return False, "belongs to other classes"

    def MTN(self):
        MTN_Irancell = self.phone.startswith(
            ('930', '933', '935', '936', '937', '938', '939', '901', '902', '903', '904', '905', '941'), 3)
        if MTN_Irancell:
            return True, "MTN_Irancell"
        return False, "belongs to other classes"

    def Rightel(self):
        Rightel = self.phone.startswith(('920', '921', '922'), 3)
        if Rightel:
            return True, "Rightel"
        return False, "belongs to other classes"

    def Talia(self):
        Talia = self.phone.startswith(('932'), 3)
        if Talia:
            return True, "Talia"
        return False, "belongs to other classes"

    def Espadan(self):
        Espadan = self.phone.startswith(('931'), 3)
        if Espadan:
            return True, "Espadan"
        return False, "belongs to other classes"

    def Kish(self):
        Kish = self.phone.startswith(('934'), 3)
        if Kish:
            return True, "Kish"
        return False, "belongs to other classes"

    def Students(self):
        Students = self.phone.startswith(('994'), 3)
        if Students:
            return True, "Students"
        return False, "belongs to other classes"

    def Shatel_virtual(self):
        Shatel_virtual = self.phone.startswith(('998'), 3)
        if Shatel_virtual:
            return True, "Shatel_virtual"
        return False, "belongs to other classes"


# __________________________________________________________________________________________________


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
        A = provider_check(validated_data['Phone'])
        p_check = A.call_everything()


        user = User.objects.create(
            username=validated_data['username'],
            Phone=validated_data['Phone'],
            provider=p_check
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




