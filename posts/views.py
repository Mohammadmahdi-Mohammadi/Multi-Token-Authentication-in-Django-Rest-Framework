import random

from django.http import Http404
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
headers: { "X-CSRFToken": '{{csrf_token}}' }
from .models import Post
from .serializers import PostSerializer,ChangePasswordSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, loginserializer
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from account.models import User



class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer

  def create(self, request, *args, **kwargs):
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)
      # headers = self.get_success_headers(serializer.data)
      token, created = Token.objects.get_or_create(user=serializer.instance)
      token_list.append(token)
      print("_________________________________________")
      print(*token_list)
      print("_________________________________________")
      return Response({'token': token.key}, status=status.HTTP_200_OK)

class Login(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = loginserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request,user)
        token,created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

class Logout(APIView):
    def get(self, request, format=None):

        print(request.user.auth_token)


        token_list.remove(request.user.auth_token)
        print("_________________________________________")
        print(*token_list)
        print("_________________________________________")
        request.user.auth_token.delete()
        return Response( status=status.HTTP_200_OK)

class Logout(APIView):
    authentication_classes = (TokenAuthentication,)
    def post(self,request):
        django_logout(request)
        return Response({"msg":"logged out."},status=status.HTTP_200_OK)

class ValidatePhoneSendOTP(APIView):

    def send_otp(self,phone):
        if phone:
            key = random.randint(999, 9999)
            return key

    def post(self, request , *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(Phone=phone)
            if not user.exists():
                return Response({"Msg":"phone number not exists!"})
            else:
                key = self.send_otp(phone)
                if key:
                    pass
                else:
                    return Response({"Msg":"Sending OTP error"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"msg":" please send phone number"},status=status.HTTP_400_BAD_REQUEST)














# _________________________________________________________________________
class UserDetailAPI(APIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AllowAny,)

token_list = []


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

    def put(self,request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class  RevokeToken(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request):
        request.auth.delete()
        return Response({"msg":"Token Revoked for: "})




class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    # model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get

            if serializer.data.get("new_password") == serializer.data.get("new_pass_repeat"):
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                token, created = Token.objects.get_or_create(user=self.get_object())

                return Response({'token': token.key},status=status.HTTP_200_OK)


            else:
                return Response({"old_password": ["repeat pass is not the same as the new password"]}, status=status.HTTP_400_BAD_REQUEST)

            # django_login(request, self.object)
            # token, created = Token.objects.get_or_create(user=serializer.instance)
            # return Response({'token': token.key},status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ___________________________________________________________________________________

from rest_framework.viewsets import ModelViewSet
class livetoken(ModelViewSet):
    # queryset = token_list.objects.all()
    # print(queryset)
    pass



# ___________________________________________________________________________________
# from django.shortcuts import render
# from django.shortcuts import get_object_or_404
# from django.http import HttpResponse
# from .models import Post,Comment
# from .Forms import PostForm
#
# from django.http import HttpResponseRedirect
# from django.http import HttpResponseNotFound
# from django.views import generic
#
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .serializers import PostSerializer

# @api_view(['GET','POST'])
# def index(request):
#     # print(request.data)
#     #body
#     # return HttpResponse('Welcome to test project')
#     # pk = request.query_params.get('pk')
#     # print(request.query_params)
#     pk = request.data.get('pk')
#     print(request.data)
#     try:
#
#         p = Post.objects.get(pk=pk)
#     except  Post.DoesNotExist:
#         return Response({'detail':'Post not exist'})
#
#     serializer = PostSerializer(p)
#     print(serializer)
#     print('-'* 100)
#     return Response(serializer.data)
#
#
#
# def post_list(request):
#     posts = Post.objects.all()
#     context = {'posts' : posts}
#     return render(request, 'posts/post_list.html', context=context)
#
#
# def post_detail(request, post_id):
#     try:
#         post = Post.objects.get(pk=post_id)
#     except Post.DoesNotExist:
#         return HttpResponseNotFound('Post is not exist!')
#     comments = Comment.objects.filter(post=post)
#     context = {'post': post, 'comments':comments}
#     return render(request, 'posts/post_detail.html', context=context)
#
#
# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'posts/post_detail.html'
#     # context_object_name = 'posts'
#     #
#     # def get_queryset(self):
#     #     return get_object_or_404(  )
#     def get_context_data(self, **kwargs):
#         context = super(PostDetail, self).get_context_data()
#         context['comments'] = Comment.objects.filter(post=kwargs['object'].pk)
#         return context
#
#
# def post_create(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             print(type(form.cleaned_data))
#             print(form.cleaned_data)
#             Post.objects.create(**form.cleaned_data)
#             return HttpResponseRedirect('/posts/')
#
#     else:
#         form = PostForm()
#
#     return render(request , 'posts/post_create.html', {'form': form})


# _____________________________________________________________
