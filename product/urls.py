from .views import ProductListAPIView, ProductItamAPIView, AddRate, AllComments, CheckComment
from django.urls import path
urlpatterns = [
    path('list/', ProductListAPIView.as_view()),
    path('get/<int:pk>', ProductItamAPIView.as_view()),
    path('score/add/<int:pk>/', AddRate.as_view()),
    path('allcomments/', AllComments.as_view()),
    path('checkcomment/', CheckComment.as_view()),
]
