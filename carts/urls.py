from django.urls import path
from .views import AddProduct, CartView, RemoveFromCart, ShoppingAPIView, TrackList, TrackDetails, CartDetailView

urlpatterns = [
    path('add/', AddProduct.as_view()),
    path('view/', CartView.as_view()),
    path('remove/', RemoveFromCart.as_view()),
    path('shop/', ShoppingAPIView.as_view()),
    path('tracklist/', TrackList.as_view()),
    path('trackdetails/<int:tracking_id>/', TrackDetails.as_view(), name='cartdetail'),
    path('cartdetail/<int:cart_id>/', CartDetailView.as_view()),
    ]