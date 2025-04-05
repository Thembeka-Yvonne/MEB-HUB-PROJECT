from django.shortcuts import render
from login.models import Campus
from bus.models import ScheduleCode,Bus_schedule,Bus
from .models import Admin_Action
from django.http import HttpResponseRedirect,HttpResponse
from datetime import datetime,timedelta


# Create your views here.
def admin_home(request):
  return render(request,"admin/admin.html")

#campus functionalilities

def campus_menu(request):
  return render(request,"admin/campus/campus_menu.html")

def add_campus(request):
  if request.method == 'POST':
    # campus_id = request.POST['campus_id']
    campus_name = request.POST['campus_name']
    campus_loc = request.POST['campus_location']
    
    # if not Campus.objects.all().filter(campus_id=campus_id).exists():
    campus = Campus(campus_name=campus_name,location=campus_loc)
    campus.save()
      # action = Admin_Action(action_type="Add Campus",admin_id=)
    return HttpResponseRedirect(redirect_to='add_campus')
  else:
   return render(request,"admin/campus/add_campus.html")
 
 
def list_all_campus(request):
  campus_list = Campus.objects.all()
  return render(request,"admin/campus/remove_campus.html",{
    "campus_list": campus_list
  })
  
def remove_campus(request,id):
  campus = Campus.objects.all().get(campus_id=id)
  campus.delete()
  return HttpResponseRedirect(redirect_to='/administration/list_all_campus')
  
  
def modify_list_campus(request):
  campus_list = Campus.objects.all()
  return render(request,"admin/campus/modify_campus.html",{
    "campus_list" : campus_list
  })
  
  
def modify_campus(request,id):
  
  campus = Campus.objects.all().get(campus_id=id)
  
  if request.method == 'POST':
    
    camp_name = request.POST['name']
    camp_loc = request.POST['location']
    
    campus.campus_name = camp_name
    campus.location = camp_loc
    
    campus.save()
    
    return HttpResponseRedirect(redirect_to='/administration/modify_list_campus')
  
  else:
    
    return render(request,"admin/campus/modify_initial_campus.html",{
      "campus": campus
    })

  
def view_all_campuses(request):
  list = Campus.objects.all()
  return render(request,"admin/campus/view_all_campuses.html",{
    "list": list
  })


#bus functionalities
def bus_menu(request):
  return render(request,"admin/buses/bus_menu.html")

def add_all_campuses_view(request):
  list = ScheduleCode.objects.all()
  return render(request,"admin/buses/add_all_camp.html",{
    "list": list
  })
  
def add_bus_schedule(request,code):
  
  schedule_c = ScheduleCode.objects.all().get(schedule_code=code)
  bus_list = Bus.objects.all()
  
  if request.method == 'POST':
    
    bus = Bus.objects.all().get(bus_id=int(request.POST['bus']))
    start_time = request.POST['start_time']
    last_time = request.POST['last_time']
    duration = int(request.POST['duration'])
      
    s_time = datetime.strptime(start_time, '%H:%M')
    l_time = datetime.strptime(last_time, '%H:%M')
    
    Bus_schedule.objects.filter(schedule_code=code).delete()
    
    n_time = datetime.strptime(start_time, '%H:%M')
      
    while n_time < l_time:
      
      n_time = s_time + timedelta(hours=duration)
      
      bus_s = Bus_schedule(departure=schedule_c.campus1,destination=schedule_c.campus2,
                             departure_time=s_time.time(),arrival_time=n_time.time(),duration=duration,
                             bus_id=bus,schedule_code=schedule_c)
        
      bus_s.save()
        
      s_time = n_time + timedelta(hours=duration)
      n_time = s_time + timedelta(hours=duration)
      
      if n_time > l_time:
        break
  
      bus_s = Bus_schedule(departure=schedule_c.campus2,destination=schedule_c.campus1,
                        departure_time=s_time.time(),arrival_time=n_time.time(),duration=duration,
                        bus_id=bus,schedule_code=schedule_c)
      bus_s.save()
        
      s_time = n_time + timedelta(hours=duration)
        
        
    return HttpResponseRedirect(redirect_to='/administration/bus_menu')
      
  else:
    return render(request,"admin/buses/add_schedule.html",{
      "schedule": schedule_c,
      "bus_list": bus_list
    })
  
  

def events_menu(request):
  return render(request,"admin/events/events_menu.html")