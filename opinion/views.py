from django.shortcuts import render

# Create your views here.
# from requests import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response

from product.models import Product
from .serializers import AddCommentSerializer,ListCommentSerializer,ProductscoreSerializer


class AddComment(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddCommentSerializer

    def post(self, request, *args, **kwargs):
        current_user = request.user.id
        print(self.kwargs.get('pk'))
        current = self.get_serializer(data=request.data)
        current.context['PID'] = self.kwargs.get('pk')
        current.is_valid(raise_exception=True)
        return Response("Comment added successfully",status=status.HTTP_200_OK)


class ListComment(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ListCommentSerializer

    def get(self, request, *args, **kwargs):
        current = self.get_serializer(data=request.data)
        current.context['PID'] = self.kwargs.get('pk')
        current.is_valid(raise_exception=True)
        current_result = ListCommentSerializer.result
        ListCommentSerializer.array_cleaner(self.serializer_class)
        return Response(current_result,status=status.HTTP_200_OK)


class ProductScoreAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductscoreSerializer
    permission_classes = [AllowAny,]