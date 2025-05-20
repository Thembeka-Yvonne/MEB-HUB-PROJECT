from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import messages
from administration.models import Admin_Action
from .models import Student, RegisteredStudent, Admin
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect
from datetime import date
from django.urls import reverse
import re
from django.utils import timezone
from django.db.models.functions import TruncDate
from bus.models import ScheduleCode
from events.models import Event

# Create your views here.
def landing(request):
    return render(request,"login/landing_page.html")
def login(request):
    if request.method == 'POST':

        username = request.POST['email']
        password = request.POST['password']

        if Student.objects.filter(studentEmail=username).exists() or Admin.objects.filter(email=username).exists():

            if "@tut4life.ac.za" in username:

                try:
                    stud = Student.objects.all().get(studentEmail=username)
                    
                    if stud.password == password:
                        request.session['stud_id'] = stud.studentNumber
                        stud.login_time = timezone.now()
                        stud.save()
                        return redirect("account:home")
                        
                    else:
                        messages.error(request, "Incorrect Password!")
                        return redirect("account:login")

                except:
                    messages.error(request, "Incorrect Username")
                    return redirect("account:login")

            elif "@mebhub.ac.za" in username:
                try:

                    admin = Admin.objects.all().get(email=username)

                    try:
                        today = timezone.localdate()
                        actions = Admin_Action.objects.annotate(action_date=TruncDate('datetime')).filter(admin_id=admin.admin_id, action_date=today)
                        events = Event.objects.filter(date__year=today.year, date__month=today.month)
                        cnt_routes=ScheduleCode.objects.count()
                    except Exception as e:
                        print(f"Error fetching actions or events: {e}")
                        actions = None
                        events=None

                    if admin.password == password:


                        request.session["admin_id"] = admin.admin_id

                        initials = f"{admin.name[0].upper()}{admin.surname[0].upper()}"
                        request.session["initials"]=initials

                        return render(request, "admin/admin.html", {
                        "admin": admin,
                        "actions": actions,
                        "events":events,
                        "initials":initials,
                        "cnt_routes":cnt_routes
                        })
                    else:
                        
                        messages.error(request, "Incorrect Password!")
                        return redirect("account:login")
                except:
                    messages.error(request, "Incorrect Username")
                    return redirect('account:login')
        else:
            
            messages.error(request, 'Account does not exist!')
            return redirect('account:login')
    else:
        return render(request, 'login/login.html')


def register(request):
    if request.method == 'POST':
        student_no = request.POST['student_no']
        name = request.POST['name']
        surname = request.POST['surname']
        student_email = request.POST['student_email']
        password = request.POST['password']
        password_confirmation = request.POST['confirm_password']
        
        pattern =  "@tut4life.ac.za"
        
        if (name == '' or surname == '' or student_email ==  '' 
           or password == '' or password_confirmation == ''):
            messages.error(request,"Fill all data fields!")
            return redirect('/login/register')
        
        if len(password) < 8 :
            messages.error(request,"Password Length > 8")
            return redirect('/login/register')
        
        if not re.search(pattern,student_email):
            messages.error(request,"Use TUT student email")
            return redirect('/login/register')
        

        if RegisteredStudent.objects.filter(studentNumber=student_no).exists():
            if password == password_confirmation:
                camp_id = RegisteredStudent.objects.all().get(studentNumber=student_no).campus_id
                student = Student(studentNumber=student_no, name=name, surname=surname,
                                studentEmail=student_email, password=password,
                                campus_id=camp_id)
                student.save()
                messages.success(request,"Account Created!")
                return redirect("/login/register")
            else:
                messages.error(request,"password not matching")
                return redirect('/login/register')
        else:
            messages.error(request,"Not a TUT registered student")
            return redirect('/login/register')

    else:
        return render(request, "login/register.html")


def admin(request):
    return render(request, "login/admin.html")

def logout_view(request):
    logout(request)
    return redirect('account:landing')

def home(request):
    stud = Student.objects.all().get(studentNumber=request.session['stud_id'])
    initials = f"{stud.name[0].upper()}{stud.surname[0].upper()}"
    request.session["initials"] = initials
    return render(request,"home/home.html",{
      "email": stud,
      "initials": initials })
    
def about(request):
    return render(request,'about_us/about_us.html')
def contact(request):
    return render(request, 'contact_us/contact_us.html')



def update_profile(request):
        stud_id = request.session.get("stud_id")
        student = Student.objects.get(studentNumber=stud_id)
        initials=request.session.get("initials")

        if request.method == 'POST':
            student = Student.objects.get(studentNumber=stud_id)
            student.name = request.POST.get('name')
            student.surname = request.POST.get('surname')

            if student.name or student.surname:
                initials = f"{student.name[0].upper()}{student.surname[0].upper()}"
                request.session["initials"] = initials

            student_password= request.POST.get('password')
            if student_password:
                student.password=student_password

            student.save()
            messages.success(request, "Profile updated successfully! 🎉")

            # Redirect with actual student email in query param
            url = reverse('account:update_profile')
            return redirect(f'{url}?initials={initials}')


        return render(request, 'home/update_profile.html', {'student': student, 'initials': initials})
