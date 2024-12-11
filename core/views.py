from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework import status
from .serializers import *
import random
from .utils import send_code_mail
class CustomObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.active_for_verify = True
        user.code = random.randint(10000, 99999)
        # send verify code 
        send_code_mail(user.email, user.code)

        # save user and return data
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class VerifyUserApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request,user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found.',},status=status.HTTP_400_BAD_REQUEST)
        
        code = request.data.get('code')
        # verify code 
        if user.active_for_verify:
            if str(user.code) == str(code):
                user.is_active = True
                user.active_for_verify = False
                user.save()
                return Response({'message': 'User is active.',},status=status.HTTP_200_OK)
            else:
                return Response({'message': 'The code is incorrect.',},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'process not found.',},status=status.HTTP_400_BAD_REQUEST)


