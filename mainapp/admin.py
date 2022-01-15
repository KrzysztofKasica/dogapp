from django.contrib import admin

# Register your models here.
from .models import Dogs, User

admin.site.register(User)
admin.site.register(Dogs)