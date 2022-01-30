from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

from .models import Bookings, Dogs, ServicesInfo, User,AdditionalInformation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email','passHash','type','active',
        )

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'password', 'createdAt', 'type', 'uid'
        )
        extra_kwargs = {'password': {'write_only':True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(label=_("Password"))

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfilePostSerializer(serializers.Serializer):
       firstname = serializers.CharField(label=_("Firstname"))
       surname = serializers.CharField(label=_("Surname"))
       phone = serializers.CharField(label=_("Phone"))
       desc = serializers.CharField(label=_("Desc"))
       lat = serializers.CharField(label=_("Latitude"))
       lon = serializers.CharField(label=_("Londitude"))
       city = serializers.CharField(label=_("City"))

class AdditionalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInformation
        fields = '__all__'

class DogGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dogs
        fields = (
            'id','name', 'race', 'birth', 'size', 'desc', 'gender', 'createdAt'
        )

class DogPostSerializer(serializers.Serializer):
    name = serializers.CharField(label=_('Name'))
    race = serializers.CharField(label=_('Race'))
    birth=serializers.DateField(label=_('Birth'), input_formats=['%Y-%m-%d'])
    size=serializers.CharField(label=_('Size'))
    desc=serializers.CharField(label=_('Description'))
    gender=serializers.CharField(label=_('Gender'))

class ServicesGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicesInfo
        #fields = '__all__'
        fields = (
            'type', 'maxSize', 'daysOfWeek', 'time', 'active', 'price'
        )

class ServicesPostSerializer(serializers.Serializer):
    type=serializers.CharField(label=_('Type'))
    maxSize=serializers.CharField(label=_('MaxSize'))
    daysOfWeek=serializers.CharField(label=_('DaysOfWeek'))
    time=serializers.CharField(label=_('Time'))
    active=serializers.CharField(label=_('Active'))
    price=serializers.IntegerField(label=_('Price'))

class BookingsPostSerializer(serializers.Serializer):
    sitterId = serializers.CharField(label=_('SitterId'))
    dogId = serializers.CharField(label=_('DogId'))
    lat = serializers.CharField(label=_('Latitude'))
    lon = serializers.CharField(label=_('Longitude'))
    time_start = serializers.CharField(label=_('TimeStart'))
    time_end = serializers.CharField(label=_('TimeEnds'))

class BookingsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = (
            'ownerId', 'sitterId', 'dogId', 'lat', 'lon', 'time_start', 'time_end'
        )

class MyTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

#class ServicesSerializer(serializers.MidelSerializer):
#    class Meta:
#s=s        model =

#test
