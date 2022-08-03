from rest_framework import response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CartItem, Cart, Shopping
from .serializers import add_product_serilizer, CartViewSerializer, RemoveFromCartSerializer, TrackListSerializer, \
    TrackDetailSerializer, CartDetailllllViewSerializer
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
import random

token_list = []


class AddProduct(generics.UpdateAPIView):
    # authentication_classes = (MultiTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # permission_classes = (AllowAny,)
    serializer_class = add_product_serilizer

    def post(self, request, *args, **kwargs):
        current_user = request.user.id
        # print("requst: ",request.user)
        # serializer = add_product_serilizer(data=request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.context["user_request"]=current_user
        serializer.is_valid(raise_exception=True)
        array_temp = add_product_serilizer.response_array
        add_product_serilizer.array_cleaner(self.serializer_class)
        return Response({'token': array_temp}, status=status.HTTP_200_OK)


class CartView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartViewSerializer

    def get_queryset(self):
        objects = Cart.objects.filter(user=self.request.user,ordered=False)
        # print(objects.first().ordered)
        my_cart = CartItem.objects.filter(cart__in=objects)
        return my_cart


class RemoveFromCart(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RemoveFromCartSerializer

    def get_queryset(self):
        objects = Cart.objects.filter(user=self.request.user)
        my_cart = CartItem.objects.filter(cart__in=objects)
        return my_cart

    def post(self, request, *args, **kwargs):
        current_user = request.user.id
        serializer = self.serializer_class(data=request.data)
        serializer.context["user_request"]=current_user
        serializer.is_valid(raise_exception=True)
        ramove_list = serializer.validated_data['ramove_list']
        ramove_list.delete()
        return Response("items deleted successfully",status=status.HTTP_200_OK)


class ShoppingAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if  Cart.objects.filter(user=self.request.user,ordered=False).first() is not None:
            # ojj = CartItem.objects.filter(cart__in=Cart.objects.filter(user=self.request.user,ordered=False))
            object = Cart.objects.filter(user=self.request.user,ordered=False).first()
            print(object)
            return object
        else:
            raise NotFound()

    def post(self, request, *args, **kwargs):
        tracking_id = random.randint(9999, 99999)
        Shopping.objects.get_or_create(cart=self.get_queryset(),tracking_id=tracking_id)
        obj = self.get_queryset()
        obj.ordered = True
        obj.save()
        print(tracking_id)
        return Response("The purchase was made successfully ========= tracking id : "+ str(tracking_id))


class TrackList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TrackListSerializer

    def get_queryset(self):
        carts = Cart.objects.filter(user=self.request.user)
        queryset = Shopping.objects.filter(cart__in=carts)
        return queryset


class TrackDetails(generics.RetrieveAPIView):
    serializer_class = TrackDetailSerializer
    lookup_field = "tracking_id"

    def get_queryset(self):
        carts = Cart.objects.filter(user=self.request.user)
        print(carts)
        queryset = Shopping.objects.filter(cart__in=carts.values_list('id',flat=True))
        return queryset


class CartDetailView(generics.ListAPIView):
    serializer_class = CartDetailllllViewSerializer
    lookup_field = 'cart_id'

    def get_queryset(self):
        usercarts = Cart.objects.filter(user=self.request.user)
        queryset = CartItem.objects.filter(cart__in=usercarts,cart=self.kwargs.get('cart_id'))
        return queryset
