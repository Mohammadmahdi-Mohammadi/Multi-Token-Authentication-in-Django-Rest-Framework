from django.contrib import admin
from django.urls import path, include, re_path
from .views import add_product
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    # path('add/', KillTokensAPIView.as_view()),
    path('add/', add_product.as_view()),

    ]