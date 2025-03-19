from django.shortcuts import render
from .models import Bus_schedule,ScheduleCode

# Create your views here.s
def home(request):
    list = ScheduleCode.objects.all()
    return render(request,"buses/home.html",{
        "list": list
    })

def view_schedule(request,schedule_code):
    list = Bus_schedule.objects.filter(schedule_code=schedule_code)

    return render(request,"buses/view_schedule.html",{
        "list": list
    })
