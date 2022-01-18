from sys import maxsize
from django.shortcuts import render
from django.http import HttpResponse, request
from rest_framework import serializers, status
from rest_framework import response
import datetime
# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .serializers import DogPostSerializer, ServicesGetSerializer, ServicesPostSerializer, UserSerializer, UserRegisterSerializer, UserLoginSerializer, DogGetSerializer
from .models import Dogs, ServicesInfo, User

class TestView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        qs = User.objects.all()
        serializer = UserSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if  serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class RegisterUserView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

class LoginUserView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data

            try:
                email = data['email']
                password = data['password']
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.get(email=email, password=password)
            except:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            try:
                user_token = user.auth_token.key
            except:
                user_token = Token.objects.create(user=user)
                user_token = user.auth_token.key
            return Response(data = {'access_token': user_token}, status=status.HTTP_200_OK)
        return Response(serializer.errors)

class GetProfile(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            token = token[6:]
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


        try:
            user = Token.objects.get(key=token).user
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        email = user.email
        password = user.password
        accType = user.accType
        active = user.active
        createdAt = user.createdAt

        return Response(data={'email': email, 'password': password, 'accType': accType, 'active': active, 'createdAt': createdAt}, status=status.HTTP_200_OK)

class DogGetPost(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            token = token[6:]
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Token.objects.get(key=token).user
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        dogs = Dogs.objects.filter(userId=user)
        serializer = DogGetSerializer(dogs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        serializer = DogPostSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = request.META.get('HTTP_AUTHORIZATION')
                token = token[6:]
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                user = Token.objects.get(key=token).user
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                data=request.data
                name=data['name']
                race=data['race']
                birth=data['birth']
                size=data['size']
                desc=data['desc']
                gender=data['gender']
                dog = Dogs(userId=user, name=name, race=race, birth=birth, size=size, desc=desc, gender=gender)
                dog.save()
            except:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            return Response(data={'name': name,  'race': race, 'birth': birth, 'size': size, 'desc': desc, 'gender': gender}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DogGetPatchDelete(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, id, *args, **kwargs):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            token = token[6:]
            user = Token.objects.get(key=token).user
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        dog = Dogs.objects.filter(userId = user, id = id)
        serializer = DogGetSerializer(dog, many=True)
        return Response(serializer.data)

    def patch(self, request, id, *args, **kwargs):
        serializer = DogPostSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = request.META.get('HTTP_AUTHORIZATION')
                token = token[6:]
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                user = Token.objects.get(key=token).user
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                dog = Dogs.objects.filter(userId = user, id = id).get()
            except:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            try:
                data=request.data
                dog.name=data['name']
                dog.race=data['race']
                dog.birth=data['birth']
                dog.size=data['size']
                dog.desc=data['desc']
                dog.gender=data['gender']
                dog.updatedAt = datetime.datetime.now()
                dog.save()
            except:
                return Response(statua=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            token = token[6:]
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key=token).user
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            dog = Dogs.objects.filter(userId = user, id = id).delete()
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_202_ACCEPTED)

class ServicesPostGet(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        qs = ServicesInfo.objects.all()
        serializer = ServicesGetSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ServicesPostSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = request.META.get('HTTP_AUTHORIZATION')
                token = token[6:]
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                user = Token.objects.get(key=token).user
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                data = request.data
                type = data['type']
                maxSize = data['maxSize']
                daysOfWeek = data['daysOfWeek']
                time = data['time']
                active = data['active']
                price = data['price']
                service = ServicesInfo(userId=user, type=type, maxSize=maxSize, daysOfWeek=daysOfWeek, time=time, active=active, price=price)
                service.save()
            except:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            return Response(data={'type': type, 'maxSize': maxSize, 'daysOfWeek': daysOfWeek, 'time': time, 'active': active, 'price': price}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
