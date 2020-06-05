from django.contrib import admin
from django_ace import AceWidget

from .models import UserInformation


# Register your models here.
admin.site.register(UserInformation)
