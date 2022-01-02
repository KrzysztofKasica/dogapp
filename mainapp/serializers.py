from rest_framework import serializers

from .models import User, Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email','passHash','accType','active',
        )


#test

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'title','description','owner'
        )