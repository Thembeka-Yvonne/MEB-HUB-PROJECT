from django.contrib import admin
from .models import Bus,Bus_schedule

from login.views import register

# Register your models here.
admin.site.register(Bus)