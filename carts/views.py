from rest_framework import response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import add_product_serilizer
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

token_list = []


class add_product(generics.UpdateAPIView):
    # authentication_classes = (MultiTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # permission_classes = (AllowAny,)
    serializer_class = add_product_serilizer


    def post(self, request, *args, **kwargs):
        current_user = request.user.id
        print("requst: ",request.user)
        # print("3333333333333333333333333333")
        # serializer = add_product_serilizer(data=request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.context["user_request"]=current_user
        serializer.is_valid(raise_exception=True)
        array_temp = []
        array_temp = add_product_serilizer.response_array
        # return serializer.data['response_array']
        # token = 2
        return Response({'token': array_temp}, status=status.HTTP_200_OK)



        # return Response({'token': token.key}, status=status.HTTP_200_OK)
