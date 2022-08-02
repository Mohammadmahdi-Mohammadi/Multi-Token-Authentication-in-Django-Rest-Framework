from django.urls import path
from .views import AddComment,ListComment,ProductScoreAPIView

urlpatterns = [

    path('add/<int:pk>/', AddComment.as_view()),
    path('list/<int:pk>/', ListComment.as_view()),
    path('score/get/<int:pk>/', ProductScoreAPIView.as_view()),

    ]