from django.shortcuts import render,redirect
from login.models import Campus,Admin
from bus.models import ScheduleCode,Bus_schedule,Bus,Bus_Stats
from .models import Admin_Action
from django.http import HttpResponseRedirect,HttpResponse
from datetime import datetime,timedelta
from datetime import date
from django.forms import Form
from events.models import Event
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.db.models import Count

# Create your views here.
def admin_home(request):
  admin = Admin.objects.all().get(admin_id=request.session['admin_id'])
  today = timezone.now().date()
  actions = Admin_Action.objects.annotate(action_date=TruncDate('datetime')).filter(admin_id=admin.admin_id,action_date=today)
  events = Event.objects.filter(date__year=today.year, date__month=today.month)
  cnt_routes=ScheduleCode.objects.count()
  context={
    "admin":admin,
    "actions" :actions,
    "events" :events,
    "initials": f"{admin.name[0].upper()}{admin.surname[0].upper()}",
    "cnt_routes":cnt_routes
  }
  return render(request,"admin/admin.html",context
  )

#campus functionalilities

#bus functionalities
def bus_menu(request):
  initials=request.session.get('initials')
  return render(request,"admin/buses/bus_menu.html",{'initials':initials})

def add_all_campuses_view(request):
  list = ScheduleCode.objects.all()
  return render(request,"admin/buses/add_all_camp.html",{
    "list": list
  })
  
def add_bus_schedule(request,code):
  
  schedule_c = ScheduleCode.objects.all().get(schedule_code=code)
  bus_list = Bus.objects.all()
  
  error = {}
  
  if request.method == 'POST':

    bus = Bus.objects.all().get(bus_id=int(request.POST['bus']))
    start_time = request.POST['start_time']
    last_time = request.POST['last_time']
    duration = int(request.POST['duration'])
    
    # Basic field validation
    if not bus or not start_time or not last_time or not duration:
        error['form'] = "All fields are required."
    
    s_time = datetime.strptime(start_time, '%H:%M')
    l_time = datetime.strptime(last_time, '%H:%M')
    
    
    # checking the time values
    if not error:
        s_time = datetime.strptime(start_time, '%H:%M')
        l_time = datetime.strptime(last_time, '%H:%M')

        if s_time == l_time:
           error['time'] = "Start and end time cannot be the same."
        elif s_time > l_time:
           error['time'] = "Start time must be earlier than end time."
        
        if not str(duration).isdigit() or int(duration) <= 0:
            error['duration'] = "Duration must be a positive number."
        else:
            duration = int(duration)
        
        if duration > 2:
           error['duration'] = "Duration must be between 1 and 2."

    
    if not error:
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
      addAction(admin_id=admin,record_type="Generated bus schedule",icon="bi bi-bus-front")
      return HttpResponseRedirect(redirect_to='/administration/bus_menu')
        
    else:
      return render(request,"admin/buses/add_schedule.html",{
        "schedule": schedule_c,
        "bus_list": bus_list,
        "errors": error
      })
      
  return render(request,"admin/buses/add_schedule.html",{
        "schedule": schedule_c,
        "bus_list": bus_list,
  })
  
def events_menu(request):
  Event.objects.filter(date__lt=date.today()).delete()  # automatically delete events
  admin_id = request.session.get('admin_id')
  initials = request.session.get("initials")

  if admin_id is None:
    return redirect('admin_home')  # or handle expired session

  admin = Admin.objects.select_related('campus_id').get(admin_id=admin_id)
  return render(request,"admin/events/events_menu.html",{'admin':admin,'initials':initials})

def addAction(admin_id: int,record_type: str,icon: str):
  action = Admin_Action(action_type=record_type,admin_id=admin_id, icon=icon,
                        datetime = timezone.now())
  action.save()
  

def view_all_actions(request):
  admin = Admin.objects.all().get(admin_id=request.session['admin_id'])
  today = timezone.now().date()
  actions = Admin_Action.objects.annotate(action_date=TruncDate('datetime')).filter(admin_id=admin.admin_id,
                                                                                    action_date=today)
  events = Event.objects.filter(date__year=today.year, date__month=today.month)
  cnt_routes = ScheduleCode.objects.count()
  context = {
    "admin": admin,
    "actions": actions,
    "events": events,
    "initials": f"{admin.name[0].upper()}{admin.surname[0].upper()}",
    "cnt_routes": cnt_routes
  }
  
  return render(request,"admin/admin.html",context)

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
      
      addAction(admin_id=admin,record_type="Added a new bus",icon="bi bi-bus-front")
      
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
        
        addAction(admin_id=admin,record_type="Bus has been removed",icon="bi bi-x-circle")
        
        return redirect('view_all_actions')
      else:
        return render(request,"admin/buses/remove_bus.html",{
          "form": form
        })

   bus_list = Bus.objects.all()
   return render(request,"admin/buses/remove_bus.html",{
     "bus_list": bus_list
   })

def bus_schedule_stats(request):
  total_views = Bus_Stats.objects.count()

  # Views per schedule
  views_per_schedule = Bus_Stats.objects.values(
    'schedule_code__schedule_code',
    'schedule_code__campus1',
    'schedule_code__campus2'
  ).annotate(view_count=Count('id')).order_by('-view_count')

  # Views by day
  views_by_day = Bus_Stats.objects.annotate(
    date=TruncDate('viewed_at')
  ).values('date').annotate(count=Count('id')).order_by('date')

  # Views in the last 7 days
  seven_days_ago = timezone.now() - timedelta(days=7)
  recent_views = Bus_Stats.objects.filter(viewed_at__gte=seven_days_ago).annotate(
    date=TruncDate('viewed_at')
  ).values('date').annotate(count=Count('id')).order_by('date')

  # Prepare data for charts
  schedule_labels = [
    f"{item['schedule_code__schedule_code']} - {item['schedule_code__campus1']} and {item['schedule_code__campus2']}"
    for item in views_per_schedule
  ]
  schedule_counts = [item['view_count'] for item in views_per_schedule]

  day_labels = [item['date'] for item in views_by_day]
  day_counts = [item['count'] for item in views_by_day]

  recent_labels = [item['date'] for item in recent_views]
  recent_counts = [item['count'] for item in recent_views]

  context = {
    'total_views': total_views,
    'views_per_schedule': list(zip(schedule_labels, schedule_counts)),
    'views_by_day': list(zip(day_labels, day_counts)),
    'recent_views': list(zip(recent_labels, recent_counts)),
    'most_viewed': views_per_schedule[0] if views_per_schedule else None,
  }

  return render(request, 'admin/buses/schedule_stats.html', context)

def user_management(request):
    initials=request.session.get("initials")
    return render(request,'admin/user_management.html',{"initials":initials})

def analytics(request):
    initials=request.session.get("initials")
    return render(request,'admin/analytics.html',{'initials':initials})
      
  
