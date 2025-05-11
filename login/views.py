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
                        messages.error(request, "Inccorect Password!")
                        return redirect("account:login")

                except:
                    messages.error(request, "Inccorect Username")
                    return redirect("account:login")

            elif "@mebhub.ac.za" in username:
                try:

                    admin = Admin.objects.get(email=username)
                    
                    try:
                        actions = Admin_Action.objects.all().filter(admin_id=admin.admin_id,
                                                                datetime__date = date.today())
                    except:
                        actions = None

                    if admin.password == password:
                        
                        if "admin_id" not in request.session:
                            request.session["admin_id"] = admin.admin_id
                            
                        return render(request,"admin/admin.html",{
                            "admin": admin,
                            "actions": actions
                        })
                    else:
                        
                        messages.error(request, "Inccorect Password!")
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
    return render(request,"home/home.html",{
      "email": stud,
      "initials": initials })
    
def about(request):
    return render(request,'about_us/about_us.html')
def contact(request):
    return render(request, 'contact_us/contact_us.html')



def update_profile(request):
        studEmail = request.GET.get("studEmail")
        student = Student.objects.get(studentEmail=studEmail)
        initials = f"{student.name[0].upper()}{student.surname[0].upper()}"

        if request.method == 'POST':
            student.name = request.POST.get('name')
            student.surname = request.POST.get('surname')
            student.studentNumber = request.POST.get('student_number')

            if 'file' in request.FILES:
                student.stud_card_image = request.FILES['file']

            student.save()
            messages.success(request, "Profile updated successfully! 🎉")

            # Redirect with actual student email in query param
            url = reverse('account:update_profile')
            return redirect(f'{url}?studEmail={student.studentEmail}')

        return render(request, 'home/update_profile.html', {'student': student, 'initials': initials})
