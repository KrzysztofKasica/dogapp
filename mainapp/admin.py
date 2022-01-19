from django.contrib import admin

# Register your models here.
from .models import Dogs, ServicesInfo, User, AdditionalInformation

admin.site.register(User)
admin.site.register(Dogs)
admin.site.register(ServicesInfo)
admin.site.register(AdditionalInformation)
