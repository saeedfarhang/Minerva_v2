from django.shortcuts import render
from django.contrib.auth import get_user_model
USER = get_user_model()
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework import permissions
from .serializers import UserSerializer
# Create your views here.

class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        data = request.data
        email = data['email']
        name = data['name']
        password = data['password']
        password2 = data['password2']

        if USER.objects.filter(email = email).exists():
            return Response({'error':'this email already exists!'}, HTTP_400_BAD_REQUEST)
        else:
            if password == password2:
                if len(password) < 6:
                    return Response({'error': 'password is too short. it must have 6 characters or or more'}, HTTP_400_BAD_REQUEST)
                else:
                    user = USER.objects.create_user(email = email, name = name, password = password)
                    user.save()
                    return Response({'success':'user been created!'}, HTTP_200_OK)
            else:
                return Response({'error':'passwords didnt match'}, HTTP_400_BAD_REQUEST)

class UserView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)