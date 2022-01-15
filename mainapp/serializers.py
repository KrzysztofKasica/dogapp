from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from .models import Dogs, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email','passHash','accType','active',
        )

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'password', 'accType'
        )

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(label=_("Password"))

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class DogGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dogs
        fields = (
            'id', 'userId', 'name', 'race', 'birth', 'size', 'desc', 'gender', 'createdAt'
        )

class DogPostSerializer(serializers.Serializer):
    name = serializers.CharField(label=_('Name'))
    race = serializers.IntegerField(label=_('Race'))
    birth=serializers.DateField(label=_('Birth'), input_formats=['%Y-%m-%d'])
    size=serializers.IntegerField(label=_('Size'))
    desc=serializers.CharField(label=_('Description'))
    gender=serializers.IntegerField(label=_('Gender'))

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
