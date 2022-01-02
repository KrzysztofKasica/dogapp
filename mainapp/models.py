from django.db import models
#from django.contrib.gis.db import models
from django.db.models.fields import CharField, DateField, DateTimeField, TimeField
from django.contrib.auth import get_user_model

CustomU = get_user_model()
# Create your models here.

class User(models.Model):
    email = models.CharField(max_length=45)
    passHash = models.CharField(max_length=255)

    class UserType(models.TextChoices):
        OWNER = '1'
        SITTER = '2'

    accType = models.CharField(max_length=1, choices=UserType.choices)

    class activeHash(models.TextChoices):
        ACTIVE = '0'
        NONACTIVE = '1'

    active = models.CharField(max_length=1, choices=activeHash.choices)
    #activeHash = models.CharField(max_length=255)
    #rememberToken = models.CharField(max_length=255, blank=True)
    #rememberAt = DateTimeField(null=True, blank=True)
    createdAt = DateTimeField(auto_now_add=True)
    #updatedAt = DateTimeField()
    #deletedAt = DateTimeField()
    
    def __str__(self):
        return self.email

class Dogs(models.Model):
    userId = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=45)
    
    class Race(models.TextChoices):
        LABRADOR = '1'
        KUNDEL = '2'
        # rasy itd...
    
    race = models.CharField(max_length=2, choices=Race.choices)
    birth = DateField()

    class Size(models.TextChoices):
        FIFTEEN = '15'
        TWENTY = '20'
        TWENTYFIVE = '25'
        THIRTY = '30'    

    size = models.CharField(max_length=2, choices=Size.choices)
    desc = models.CharField(max_length=255)
    createdAt = DateTimeField(auto_now_add=True)
    
    class Gender(models.TextChoices):
        MALE = '0'
        FEMALE = '1'

    gender = models.CharField(max_length=1, choices=Gender.choices)

    def __str__(self):
        return self.name

class AdditionalInformation(models.Model):
    userId = models.ForeignKey('User', on_delete=models.CASCADE)
    firstName = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    #place = models.PointField()
    phone = models.CharField(max_length=35)
    desc = models.CharField(max_length=255)
    photoURL = models.CharField(max_length=255)
    createdAt = DateTimeField(auto_now_add=True)
    updatedAt = DateTimeField

    def __str__(self):
        return self.name

class ServicesInfo(models.Model):
    userId = models.ForeignKey('User', on_delete=models.CASCADE)

    class Type(models.TextChoices):
        WALKING = 'WK'
        DAY_CARE = 'DC'
    
    type = models.CharField(max_length=2, choices=Type.choices)

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
        return self.name

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
    updatedAt = DateTimeField

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

#test

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(CustomU, on_delete=models.CASCADE)

    def __str__(self):
        return self.title