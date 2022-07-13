
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from posts.views import RegisterUserAPIView,Logout,Login,ChangePasswordView, SendOTP , ValidateOTP, ForgetPassword
router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('posts/', include('posts.urls')),
    path('register/', RegisterUserAPIView.as_view()),
    path('login/',Login.as_view()),
    path('logout/', Logout.as_view()),
    path('send-otp/', SendOTP.as_view()),
    path('validate-otp/', ValidateOTP.as_view()),
    path('change-pass/', ChangePasswordView.as_view(),name='change-password'),
    path('forget-pass/', ForgetPassword.as_view(),name='Forget-password'),


    # re_path(r'^api/auth/', include('django_rest_multitokenauth.urls', namespace='multi_token_auth')),

    # path('get_token/', obtain_auth_token),

]

