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


def events_menu(request):
  return render(request,"admin/events/events_menu.html")