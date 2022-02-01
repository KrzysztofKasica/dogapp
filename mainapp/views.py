from sys import maxsize
from django.shortcuts import render
from django.http import HttpResponse, request
from rest_framework import serializers, status
from django.db.models import Q
from rest_framework import response
import datetime
from math import radians, cos, sin, asin, sqrt

# Create your views here.
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import BookingsGetSerializer, BookingsPostSerializer, DogPostSerializer, ProfileSerializer, SearchSerializer, ServicesGetSerializer, ServicesPostSerializer, UserSerializer, UserRegisterSerializer, UserLoginSerializer, DogGetSerializer, AdditionalInformationSerializer, ProfilePostSerializer
from .models import Bookings, Dogs, ServicesInfo, User, AdditionalInformation

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
                service = ServicesInfo.objects.get(userId = user)
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

class BookingsPost(APIView):

   permission_classes = (IsAuthenticated, )

   def get(self, request, *args, **kwargs):
        try:
            user=request.user
            data = Bookings.objects.filter(Q(sitterId=user) | Q(ownerId=user))
            data = data.exclude(sitterId__isnull=True)
            data = data.exclude(dogId__isnull=True)
            serializer = BookingsGetSerializer(data, many=True)
            for i, booking in enumerate(serializer.data):
                d = data[i]
                firstName = AdditionalInformation.objects.get(userId=d.sitterId).firstname
                dogName = Dogs.objects.get(id=d.dogId.id).name
                booking['dogName'] = dogName
                booking['firstName'] = firstName
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


   def post(self, request, *args, **kwargs):
        serializer = BookingsPostSerializer(data=request.data)
        if serializer.is_valid():

            try:
                user = request.user
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                data=request.data
                sitterId = User.objects.get(user_id=data['sitterId'])
                dogId = Dogs.objects.get(id=data['dogId'])
                lat = data['lat']
                lon = data['lon']
                time_start = datetime.datetime.fromtimestamp(int(data['time_start']))
                time_end = datetime.datetime.fromtimestamp(int(data['time_end']))
                price = ServicesInfo.objects.get(userId=sitterId).price
                booking = Bookings(ownerId=user, sitterId=sitterId, dogId=dogId,  lat=lat, lon=lon, time_start=time_start, time_end=time_end, status='1', price=price)
                booking.save()
            except:
                return Response(data=request.data, status=status.HTTP_400_BAD_REQUEST)
            return Response( status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class SearchView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):

        def haversine(lon1, lat1, lon2, lat2):
            """
            Calculate the great circle distance between two points
            on the earth (specified in decimal degrees)
            """
            return lon1
            # convert decimal degrees to radians
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

            # haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            # Radius of earth in kilometers is 6371
            km = 6371* c
            return km

        def daysOfWeek(days1, days2):
            days = {
                0: "1000000",
                1: "0100000",
                2: "0010000",
                3: "0001000",
                4: "0000100",
                5: "0000010",
                6: "0000001"
            }

            mydate = datetime.datetime(int(days1[:4]), int(days1[5:7]), int(days1[8:10]))
            mydate = mydate.weekday()
            days1 = days[mydate]
            days2 = str(bin(days2)[2:])

            for _ in range(7-len(days2)):
                days2 = "0" + days2

            i = days1.find("1")
            if days1[i] == days2[i]:
                return False #dont exclude
            return True #exclude


        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = request.user
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                adInfo = AdditionalInformation.objects.get(userId=user)
                lat = adInfo.lat
                lon = adInfo.lon
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                data=request.data

                services = ServicesInfo.objects.filter(active="1", price__gte=data['price_start'], price__lte=data['price_end'], maxSize__gte=data['size_dog'])
                #services = ServicesInfo.objects.all()

                for service in services:
                    searchUser = User.objects.get(user_id=service.userId.user_id)
                    adInfo = AdditionalInformation.objects.get(userId=searchUser)
                    distance = haversine(lon, lat, adInfo.lon, adInfo.lat)
                    if distance >= float(data['radius']):
                        services = services.exclude(id=service.id)
                        #service.extra(distance="12")
                        continue
                    if daysOfWeek(data['datetime_start'][:10], service.daysOfWeek):
                        services = services.exclude(id=service.id)
                        continue
                service_serializer = ServicesGetSerializer(services, many=True)

                for i, service in enumerate(service_serializer.data):

                    pass
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(data=service_serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
