from django.shortcuts import render
from login.models import Campus
from .models import Admin_Action
from django.http import HttpResponseRedirect,HttpResponse

# Create your views here.
def admin_home(request):
  return render(request,"admin/admin.html")

def campus_menu(request):
  return render(request,"admin/campus/campus_menu.html")

def add_campus(request):
  if request.method == 'POST':
    campus_id = request.POST['campus_id']
    campus_name = request.POST['campus_name']
    campus_loc = request.POST['campus_location']
    
    if not Campus.objects.all().filter(campus_id=campus_id).exists():
      campus = Campus(campus_id=campus_id,campus_name=campus_name,location=campus_loc)
      campus.save()
      # action = Admin_Action(action_type="Add Campus",admin_id=)
      return HttpResponseRedirect(redirect_to='add_campus')
    else:
      return HttpResponse('Campus id is not unique')
  else:
   return render(request,"admin/campus/add_campus.html")

def events_menu(request):
  return render(request,"admin/events/events_menu.html")