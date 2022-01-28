from sys import maxsize
from django.shortcuts import render
from django.http import HttpResponse, request
from rest_framework import serializers, status

from rest_framework import response
import datetime
# Create your views here.
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import DogPostSerializer, ServicesGetSerializer, ServicesPostSerializer, UserSerializer, UserRegisterSerializer, UserLoginSerializer, DogGetSerializer, AdditionalInformationSerializer, ProfilePostSerializer
from .models import Dogs, ServicesInfo, User, AdditionalInformation

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
            return Response(data = serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)

class TokenRefresh(APIView):
    def post(self, request, *args, **kwargs):
          def get_tokens_for_user(refresh_token):
                    refresh = RefreshToken(refresh_token)
                    #refresh['type'] = user.type
                    #refresh['email'] = user.email

                    return {
                                'refresh_token': str(refresh),
                                'access_token': str(refresh.access_token),
                    }

          data = request.data

          try:
            refresh_token = data['refresh_token']
          except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
          try:
               # get_tokens_for_user(refresh_token)
                user_token = get_tokens_for_user(refresh_token)
          except:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
          return Response(data = user_token, status=status.HTTP_200_OK)


class LoginUserView(APIView):
    def post(self, request, *args, **kwargs):
    ## GENERATE TOKENS FOR USER
        def get_tokens_for_user(user):
            refresh = RefreshToken.for_user(user)
            refresh['type'] = user.type
            refresh['email'] = user.email

            return {
                        'refresh_token': str(refresh),
                        'access_token': str(refresh.access_token),
            }

        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            try:
                email = request.data.get('email', None)
                password = request.data.get('password', None)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.get(email=email)
            except:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            try:
                user_token = get_tokens_for_user(user)
            except:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
                #user_token = get_tokens_for_user(user)
                #user_token = user.auth_token.key
            return Response(data = user_token, status=status.HTTP_200_OK)
        return Response(serializer.errors)

class GetProfile(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):

        try:
            user = self.request.user
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        additionalInformation = AdditionalInformation.objects.get(userId=user)

        email = user.email
        type = user.type
        active = user.is_active
        firstname = additionalInformation.firstname
        surname = additionalInformation.surname
        phone = additionalInformation.phone
        desc = additionalInformation.desc
        city = additionalInformation.city
        photoURL = additionalInformation.photoURL
        createdAt = user.createdAt

        return Response(data={'email': email, 'firstname':firstname,'surname':surname,'phone':phone,'desc':desc, 'photoURL':photoURL, 'type': type, 'city':city, 'active': active, 'createdAt': createdAt}, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
            serializer = ProfilePostSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    user = request.user
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                try:
                    profile = AdditionalInformation.objects.filter(userId = user).get()
                except:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
                try:
                    data=request.data
                    profile.firstname=data['firstname']
                    profile.surname=data['surname']
                    profile.phone=data['phone']
                    profile.desc=data['desc']

                    profile.lat=data['lat']
                    profile.lon=data['lon']
                    profile.city=data['city']
                    profile.updatedAt = datetime.datetime.now()
                    profile.save()
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                return Response(data={'firstname': profile.firstname,  'surname': profile.surname, 'phone': profile.phone, 'lat': profile.lat, 'lon': profile.lon,  'city': profile.city}, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DogGetPost(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        dogs = Dogs.objects.filter(userId=user)
        serializer = DogGetSerializer(dogs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        serializer = DogPostSerializer(data=request.data)
        if serializer.is_valid():

            try:
               user = request.user
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
            return Response(data={'name': name, 'id':dog.id,  'race': race, 'birth': birth, 'size': size, 'desc': desc, 'gender': gender}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DogGetPatchDelete(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, id, *args, **kwargs):

        dog = Dogs.objects.filter(userId = user, id = id)
        serializer = DogGetSerializer(dog, many=True)
        return Response(serializer.data)

    def patch(self, request, id, *args, **kwargs):
        serializer = DogPostSerializer(data=request.data)
        if serializer.is_valid():

            try:
                user = request.user
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
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(data={'id': dog.id,'name': dog.name,  'race': dog.race, 'birth': dog.birth, 'size': dog.size, 'desc': dog.desc, 'gender': dog.gender}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):

        try:
            user = request.user
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

    def patch(self, request, *args, **kwargs):
        serializer = ServicesPostSerializer(data=request.data)
        if serializer.is_valid():
            try:
               user = request.user
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                service = ServicesInfo.objects.filter(userId = user).get()
            except:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            try:
                data = request.data
                service.type = data['type']
                service.maxSize = data['maxSize']
                service.daysOfWeek = data['daysOfWeek']
                service.time = data['time']
                service.active = data['active']
                service.price = data['price']
                #service = ServicesInfo(userId=user, type=type, maxSize=maxSize, daysOfWeek=daysOfWeek, time=time, active=active, price=price)
                service.save()
            except:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            return Response(data={'type': service.type, 'maxSize': service.maxSize, 'daysOfWeek': service.daysOfWeek, 'time': service.time, 'active': service.active, 'price': service.price}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


