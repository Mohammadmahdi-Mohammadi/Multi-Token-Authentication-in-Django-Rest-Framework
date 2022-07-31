from .views import ProductListAPIView, ProductItamAPIView, AddRate, AllComments, CheckComment, AddToCart
from django.urls import path
urlpatterns = [
    path('list/', ProductListAPIView.as_view()),
    path('get/<int:pk>', ProductItamAPIView.as_view()),
    path('score/add/<int:pk>/', AddRate.as_view()),
    path('allcomments/', AllComments.as_view()),
    path('checkcomment/', CheckComment.as_view()),
    path('cart/add/', AddToCart.as_view()),
]
