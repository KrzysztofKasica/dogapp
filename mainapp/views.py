from django.shortcuts import render
from django.http import HttpResponse, request
from rest_framework import serializers
# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSerializer, PostSerializer
from .models import User, Post

class TestView(APIView):
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