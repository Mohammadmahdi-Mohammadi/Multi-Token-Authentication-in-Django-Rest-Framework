from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from product.serializers import ProductListSerializer, AddRateSerializer, AllCommentsserilizer, CheckCommentSerializer, \
    AddToCartSerializer
from .models import User, Product, Comment
from rest_framework.response import Response


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['brand','type','name']


class ProductItamAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]


class AddRate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddRateSerializer

    def put(self, request, *args, **kwargs ):
        user_name = self.request.user.username
        url = request.build_absolute_uri()
        index_item = url.split('/')[-2]
        serializer = self.get_serializer(data=request.data)
        serializer.context["rate"] = request.data['rate']
        serializer.context["product_id"] = index_item
        serializer.context["username"] = user_name
        serializer.is_valid(raise_exception=True)
        print("URL: ",index_item)
        return  Response('auishdioahsodi')


class AllComments(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AllCommentsserilizer
    def get_queryset(self):
        new_comments = Comment.objects.filter(chech_admin=False)
        return new_comments



class CheckComment(APIView):
    queryset = Comment.objects.filter(chech_admin=False)
    permission_classes = (IsAuthenticated,)
    serializer_class = CheckCommentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        comments = serializer.validated_data['comments']
        comments.update(chech_admin=True)
        return Response(status=status.HTTP_200_OK)


# class AddToCart(generics.UpdateAPIView):
#     queryset = User.objects.all()

class AddToCart(APIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AddToCartSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        products = serializer.validated_data['products']
        products += User.objects.filter(id=request.user.id).cart
        User.objects.filter(id=request.user.id).update(cart=products)
        return Response(status=status.HTTP_200_OK)