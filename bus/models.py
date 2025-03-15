from tkinter.constants import CASCADE

from django.db import models
from login.models import *

# Create your models here.
class ScheduleCode(models.Model):
    schedule_code = models.IntegerField(primary_key=True)
    
class Bus(models.Model):
    bus_id = models.IntegerField(primary_key=True)
    bus_name = models.CharField(max_length=255,null=False)
    campus_id = models.ForeignKey(Campus,on_delete=models.CASCADE)

class Bus_schedule(models.Model):
    departure = models.CharField(max_length=255,null=False)
    destination = models.CharField(max_length=255,null=False)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.IntegerField()
    bus_id = models.OneToOneField(Bus,on_delete=models.CASCADE)
    schedule_code = models.ForeignKey(ScheduleCode,on_delete=models.CASCADE)
    
