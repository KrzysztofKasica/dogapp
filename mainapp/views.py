from django.shortcuts import render
from django.http import HttpResponse, request
# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response

class TestView(APIView):
    def get(self, request, *args, **kwargs):
        date = {
            'name': 'jogn',
            'age': '23'
        }
        return Response(date)