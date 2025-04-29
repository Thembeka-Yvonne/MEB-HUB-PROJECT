from django.shortcuts import render,redirect
from login.models import Campus,Admin
from bus.models import ScheduleCode,Bus_schedule,Bus
from .models import Admin_Action
from django.http import HttpResponseRedirect,HttpResponse
from datetime import datetime,timedelta
from datetime import date
from django.forms import Form

# Create your views here.
def admin_home(request):
  admin =  Admin.objects.all().get(admin_id=request.session['admin_id'])
  return render(request,"admin/admin.html",{
    "admin": admin
  })

#campus functionalilities

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
        
    admin = Admin.objects.all().get(admin_id=request.session['admin_id'])
    addAction(admin_id=admin,record_type="Generated bus schedule")
    return HttpResponseRedirect(redirect_to='/administration/bus_menu')
      
  else:
    return render(request,"admin/buses/add_schedule.html",{
      "schedule": schedule_c,
      "bus_list": bus_list
    })
  
def events_menu(request):
  adminEmail = request.GET.get("adminEmail")
  admin = Admin.objects.select_related('campus_id').get(email=adminEmail)
  return render(request,"admin/events/events_menu.html",{'admin':admin})

def addAction(admin_id: int,record_type: str):
  action = Admin_Action(action_type=record_type,admin_id=admin_id,
                        datetime = datetime.now())
  action.save()
  

def view_all_actions(request):
  
  action = Admin_Action.objects.all().filter(admin_id=request.session['admin_id'],
                                             datetime__date = date.today())
  admin = Admin.objects.all().get(admin_id=request.session['admin_id'])
  
  return render(request,"admin/admin.html",{
    "admin": admin,
    "actions": action
  })

def add_bus(request):
  if request.method == 'POST':
    form = Form(request.POST)
    if form.is_valid():
      bus_name = request.POST["bus_name"]
      campus_id = request.POST["campus"]

      campus = Campus.objects.all().get(campus_id=campus_id)
      bus = Bus(bus_name=bus_name,campus_id=campus)

      bus.save()
      
      admin = Admin.objects.all().get(admin_id=request.session['admin_id'])
      
      addAction(admin_id=admin,record_type="Added a new bus")
      
      return redirect('view_all_actions')
    
    else:
       return  render(request,"admin/buses/add_bus_html",{
         "form": form
       })

  campus_list = Campus.objects.all()
  return render(request,"admin/buses/add_bus.html",{
    "campus_list": campus_list
  })


def remove_bus(request):
   if request.method == 'POST':
      form = Form(request.POST)
      
      if form.is_valid:
        bus_id = request.POST["bus"]

        bus = Bus.objects.all().get(bus_id=bus_id)
        
        bus.delete()
        
        admin = Admin.objects.all().get(admin_id=request.session['admin_id'])
        
        addAction(admin_id=admin,record_type="Bus has been removed")
        
        return redirect('view_all_actions')
      else:
        return render(request,"admin/buses/remove_bus.html",{
          "form": form
        })

   bus_list = Bus.objects.all()
   return render(request,"admin/buses/remove_bus.html",{
     "bus_list": bus_list
   })
       
        
  
      
  
