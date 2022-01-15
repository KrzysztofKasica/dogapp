"""dogapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import mainapp
from mainapp.views import DogGetPost, DogPatchDelete, ServicesPostGet, TestView, RegisterUserView, LoginUserView, GetProfile
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mainapp/', include('mainapp.urls')),
    path('', TestView.as_view(), name='test'),
    path('api/token', obtain_auth_token, name='obtain-token'),
    path('auth/register', RegisterUserView.as_view(), name='register'),
    path('auth', LoginUserView.as_view(), name='login'),
    path('profile', GetProfile.as_view(), name="profile"),
    path('dogs', DogGetPost.as_view(), name='getpostdogs'),
    path('dogs/<id>', DogPatchDelete.as_view(), name='patchdeletedog'),
    path('services', ServicesPostGet.as_view(), name='servicespostget')
]
