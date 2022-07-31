

# headers: {"X-CSRFToken": '{{csrf_token}}'}
import random

from .models import Post
from account.models import User
from .serializers import RegisterSerializer, loginserializer
from .serializers import PostSerializer, ChangePasswordSerializer, ForgetPasswordSerializer
from .serializers import KillTokenSerializer,ListTokenSerializer
from .authentication import MultiTokenAuthentication

from django.http import Http404
from django.core.cache import cache
from django.contrib.auth import login as django_login, logout as django_logout

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from .models import MultiTokens
token_list = []


class RegisterUserAPIView(generics.CreateAPIView):
    authentication_classes = (MultiTokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        # user_agent = request.META['HTTP_USER_AGENT']
        # if user_agent is None:
        #     Response({"Msg: User-Agent is empty! "},status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        user_agent = request.META['HTTP_USER_AGENT']
        user = serializer.instance
        token, created = MultiTokens.objects.get_or_create(user=user , counterplus =user.counter, name=user_agent)
        token_list.append(token)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class Login(APIView):
    authentication_classes = (MultiTokenAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        # user_agent = request.META['HTTP_USER_AGENT']
        # if user_agent is None:
        #     Response({"Msg: User-Agent is empty! "},status=status.HTTP_400_BAD_REQUEST)
        serializer = loginserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        user_agent = request.META['HTTP_USER_AGENT']
        user_object = User.objects.get(id=user.id)
        user_object.counter += 1
        user_object.save()
        token, created = MultiTokens.objects.get_or_create(user=user, name=user_agent, counterplus=user.counter)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class Logout(APIView):
    authentication_classes = (MultiTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        django_logout(request)
        request.auth.delete()
        return Response({"msg": "logged out."}, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    authentication_classes = (MultiTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        # user_agent = request.META['HTTP_USER_AGENT']
        # if user_agent is None:
        #     Response({"Msg: User-Agent is empty! "},status=status.HTTP_400_BAD_REQUEST)

        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            if serializer.data.get("new_password") == serializer.data.get("new_pass_repeat"):
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                user=request.user
                MultiTokens.objects.filter(user=user.id).delete()
                user_object = User.objects.get(id=user.id)
                user_object.counter += 1
                user_object.save()
                user_agent = request.META['HTTP_USER_AGENT']
                token, created = MultiTokens.objects.get_or_create(user=user, name=user_agent, counterplus=user.counter)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"old_password": ["Password repeat and new pass are not the same!"]},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)


def send_otp_pre(phone):

    if cache.get(phone):
        print("_________________________________")
        print("OTP code already sent!")
        print("try again a few minutes later :/ ")
        print("_________________________________")
        return False

    try:
        otp_to_send = random.randint(999,9999)
        print("_________________________________")
        print("OTP to send is: ",otp_to_send)
        print("_________________________________")

        cache.set(phone,otp_to_send, timeout=240)
        # user_obj.otp = otp_to_send
        # user_obj.save()
        return False
    except Exception as e:
        print(e)


def send_otp(phone, OTP):
    if cache.get(phone):
        print("phone is in the cache")
        print("cache value is: ", cache.get(phone))
        if int(cache.get(phone)) == int(OTP):
            print('phone verified with code in the cache')
            cache.delete(phone)
            return True
        return False
    return False


class SendOTP(APIView):
    authentication_classes = (MultiTokenAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('Phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(Phone=phone)
            if not user.exists():
                return Response({"Msg": "OTP sent successfully :]"}, status=status.HTTP_200_OK)
            else:
                send_otp_pre(phone_number)
                return Response({"Msg": "OTP sent successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"Phone": " please send valid phone number"}, status=status.HTTP_400_BAD_REQUEST)


class ValidateOTP(APIView):
    authentication_classes = (MultiTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        otp_code = request.data.get('OTP')
        if otp_code:
            phone = request.user.Phone
            print("__________________________________")
            print("current state summary:")
            print("PHONE NUMBER IS: ", phone)
            print("INSERTED CODE is: ", otp_code)
            print("__________________________________")
            if send_otp(phone, otp_code):
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"OTP": "Enter the OTP code"}, status=status.HTTP_400_BAD_REQUEST)


class ForgetPassword(generics.UpdateAPIView):
    authentication_classes = (MultiTokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = ForgetPasswordSerializer

    def update(self, request, *args, **kwargs):
        # user_agent = request.META['HTTP_USER_AGENT']
        # if user_agent is None:
        #     Response({"Msg: User-Agent is empty! "},status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(username=request.data.get('username')).first()
            print("phone: ",user.Phone,"OTP: ",request.data.get('OTP'))
            if send_otp(user.Phone ,request.data.get('OTP')):
                if serializer.data.get("new_password") == serializer.data.get("new_pass_repeat"):
                    u = User.objects.get(username__exact=user.username)
                    u.set_password(request.data.get('new_password'))
                    u.save()
                    print("________________________________________________")
                    print("New pass is: ", request.data.get('new_password'))
                    print("username: ", user.username)
                    print("________________________________________________")
                    user_agent = request.META['HTTP_USER_AGENT']
                    MultiTokens.objects.filter(user=user.id).delete()
                    user_object = User.objects.get(id=user.id)
                    user_object.counter += 1
                    user_object.save()
                    token, created = MultiTokens.objects.get_or_create(user=user, name=user_agent, counterplus=user.counter)
                    return Response({'token': token.key}, status=status.HTTP_200_OK)
                else:
                    return Response({"old_password": ["Password repeat and new pass are not the same!"]},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"No valid OTP for this number! "},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)


class ListTokenAPIView(generics.ListAPIView):
    authentication_classes = (MultiTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = MultiTokens.objects.all()
    serializer_class = ListTokenSerializer

    def get(self, request, *args, **kwargs):
        # user_agent = request.META['HTTP_USER_AGENT']
        # if user_agent is None:
        #     Response({"Msg: User-Agent is empty! "},status=status.HTTP_400_BAD_REQUEST)
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        requesttoken = self.request.META.get('HTTP_AUTHORIZATION')
        strs = str(requesttoken).split(" ")
        requested_token = strs[1]
        user = MultiTokens.objects.get(key=requested_token).user
        userobjects = User.objects.filter(username=user)
        userobject = userobjects.first()
        tokens = MultiTokens.objects.filter(user=userobject.id)
        return tokens


class KillTokensAPIView(APIView):
    authentication_classes = (MultiTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = MultiTokens.objects.all()
    serializer_class = KillTokenSerializer

    def post(self, request, *args, **kwargs):
        # user_agent = request.META['HTTP_USER_AGENT']
        # if user_agent is None:
        #     Response({"Msg: User-Agent is empty! "},status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data['tokens']
        tokens.delete()
        return Response(status=status.HTTP_200_OK)



# _________________________________________________________________________


class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)


class PostListView(APIView):

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    def get_object(self, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
        return post

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# _________________________________________________________________________
