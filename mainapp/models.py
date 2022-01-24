from django.db import models

#from django.contrib.gis.db import models
import uuid
from django.db.models.fields import CharField, DateField, DateTimeField, TimeField
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password, type, **extra_fields):
        if not email:
            raise ValueError("must have email")
        if not password:
            raise ValueError("must have password")
        if not type:
            raise ValueError("must have type")
        email = self.normalize_email(email)
        user = self.model(email=email, type=type, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        '''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        return self.create_user(email=email, password=password, accType=1, **extra_fields)
        '''
        user = self.create_user(email, password, 1, **extra_fields)
        user.is_admin = True
        #user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
'''
class User2(AbstractUser):
    username = None
    email = models.EmailField(max_length=45, unique=True)

    class UserType(models.TextChoices):
        OWNER = '1'
        SITTER = '2'

    accType = models.CharField(max_length=1, choices=UserType.choices)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'accType']

    def __str__(self):
        return self.email
'''
class User(AbstractUser, PermissionsMixin):
    user_id = models.BigAutoField(primary_key=True,unique=True)
    uid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    email = models.EmailField(_('email address'), unique=True)
    username = None
    #email = models.EmailField(max_length=45, unique=True)
    password = models.CharField(max_length=100)

    class UserType(models.TextChoices):
        OWNER = '1'
        SITTER = '2'

    type = models.CharField(max_length=1, choices=UserType.choices)

    class Active(models.TextChoices):
        ACTIVE = '0'
        NONACTIVE = '1'

    is_active = models.CharField(max_length=1, choices=Active.choices, default=1)
    #activeHash = models.CharField(max_length=255)
    #rememberAt = DateTimeField(null=True, blank=True)
    createdAt = DateTimeField(auto_now_add=True)
    is_staff = True
    #updatedAt = DateTimeField()
    #deletedAt = DateTimeField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = UserManager()

    def __str__(self):
        return self.email

class Dogs(models.Model):
    userId = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=45)


    race = models.CharField(max_length=45)
    birth = DateField()

    size = models.CharField(max_length=3)
    desc = models.CharField(max_length=255)
    createdAt = DateTimeField(auto_now_add=True)

    class Gender(models.TextChoices):
        MALE = 'pies'
        FEMALE = 'suka'

    gender = models.CharField(max_length=4, choices=Gender.choices)

    def __str__(self):
        return self.name

class AdditionalInformation(models.Model):
    userId = models.ForeignKey('User', on_delete=models.CASCADE)
    firstname = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
   # place = models.PointField()
    phone = models.CharField(max_length=35)
    desc = models.CharField(max_length=255)
    photoURL = models.CharField(max_length=255)
    createdAt = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField

    def __str__(self):
        return self.firstname

class ServicesInfo(models.Model):
    userId = models.ForeignKey('User', on_delete=models.CASCADE)

    class Type(models.TextChoices):
        WALKING = 'WK', _("WALKING")
        DAY_CARE = 'DC'

    type = models.CharField(max_length = 2, choices=Type.choices)

    class MaxSize(models.TextChoices):
        FIFTEEN = '15'
        TWENTY = '20'
        TWENTYFIVE = '25'
        THIRTY = '30'

    maxSize = models.CharField(max_length=2, choices=MaxSize.choices)

    class DaysOfWeek(models.TextChoices):
        MONDAY = '1'
        TUESDAY = '2'
        WENDESDAY = '3'
        THURSDAY = '4'
        FRIDAY = '5'
        SATURDAY = '6'
        SUNDAY = '7'

    daysOfWeek = models.CharField(max_length=1, choices=DaysOfWeek.choices)

    class Time(models.TextChoices):
        MORNING = '1'
        AFTERNOON = '2'
        EVENING = '3'

    time = models.CharField(max_length=1, choices=Time.choices)

    class Active(models.TextChoices):
        ACTIVE = '0'
        NONACTIVE = '1'

    active = models.CharField(max_length=1, choices=Active.choices)
    price = models.IntegerField()

    def __str__(self):
        return str(self.id)

class Bookings (models.Model):
    ownerId = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='owner')
    dogId = models.ForeignKey('Dogs', on_delete=models.SET_NULL, null=True)
    sitterId = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='sitter')
    hashId = models.CharField(max_length=255)
    title = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    #location = models.PointField()
    time_start = DateTimeField()
    time_end = DateTimeField()

    class Status(models.TextChoices):
        PENDING = '0'
        UNDERWAY = '1'
        COMPLETED = '2'

    status = models.CharField(max_length=1, choices=Status.choices)
    cancelReaseon = models.CharField(max_length=255, blank=True)
    createdAt = DateTimeField()
    updated_at = DateTimeField

    def __str__(self):
        return self.name

class MessagesUsers(models.Model):
    userFrom = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='sender')
    userTo = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='reciever')
    text = models.CharField(max_length=255)

    class Status(models.TextChoices):
        #nw o jakie statusy tu chodzilo
        STATUSZERO = '0'
        STATUSONE = '1'

    status = models.CharField(max_length=1, choices=Status.choices)
    createdAt = DateTimeField(auto_now_add=True)

