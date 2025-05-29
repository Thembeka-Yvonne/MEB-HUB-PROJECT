from django.db import models
from login.models import  Admin
from django.utils import timezone

# Create your models here.


def default_time():
    return timezone.now().time()

class Event(models.Model):
    event_id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=1000)
    date = models.DateField()
    image = models.BinaryField(editable=True,null=False,default=b'\x00')
    location = models.CharField(max_length=255)
    admin_id = models.ForeignKey(Admin,on_delete=models.CASCADE)
    start_time = models.TimeField(null=True,default=default_time)
    end_time = models.TimeField(null=True,default=default_time)
    attendance_count = models.IntegerField(null=True)
    capacity=models.IntegerField(null=True)


    def __str__(self):
        return f"{self.event_id} {self.location} {self.date}"
    
    
class RSVP(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=255)
    guest_surname = models.CharField(max_length=255)
    guest_studentnumber = models.CharField(max_length=255)
