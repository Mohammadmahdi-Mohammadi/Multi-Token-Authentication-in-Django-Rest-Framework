from django.urls import path

from .views import PostListView,PostDetailView,UserDetailAPI,RegisterUserAPIView

urlpatterns = [

    path('', PostListView.as_view()),
    path('<int:pk>/',PostDetailView.as_view()),
    path("get-details", UserDetailAPI.as_view()),


]



