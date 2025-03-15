from django.db import models
from login.models import  Admin

# Create your models here.
class Event(models.Model):
    event_id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=1000)
    date = models.DateField()
    image = models.ImageField(upload_to="event_images",null=True)
    location = models.CharField(max_length=255)
    admin_id = models.ForeignKey(Admin,on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.event_id} {self.location} {self.date}"
