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
from mainapp.views import BookingsPost, DogGetPost, DogGetPatchDelete, SearchView, ServicesPostGet, TestView, RegisterUserView, LoginUserView, GetProfile, TokenRefresh
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mainapp/', include('mainapp.urls')),
    path('', TestView.as_view(), name='test'),
    #path('api/token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh', TokenRefresh.as_view(), name='token_refresh'),
    path('auth/register', RegisterUserView.as_view(), name='register'),
    path('auth', LoginUserView.as_view(), name='login'),
    path('profile', GetProfile.as_view(), name="profile"),
    path('dogs', DogGetPost.as_view(), name='getpostdogs'),
    path('dogs/<id>', DogGetPatchDelete.as_view(), name='getpatchdeletedog'),
    path('services', ServicesPostGet.as_view(), name='servicespostget'),
    path('bookings', BookingsPost.as_view(), name='bookingspost'),
    path('sitters/search', SearchView.as_view(), name='search')
]
