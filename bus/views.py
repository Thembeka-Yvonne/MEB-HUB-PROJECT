from django.shortcuts import render
from .models import Bus_schedule

# Create your views here.
def home(request):
    return render(request,"buses/home.html")

def view_schedule(request,schedule_code):
    list = Bus_schedule.objects.filter(schedule_code=schedule_code)

    return render(request,"buses/view_schedule.html",{
        "list": list
    })
