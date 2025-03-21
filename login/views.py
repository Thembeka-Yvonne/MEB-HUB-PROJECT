from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import messages

from .models import Student, RegisteredStudent, Admin


# Create your views here.
def login(request):
    if request.method == 'POST':

        username = request.POST['email']
        password = request.POST['password']

        if Student.objects.filter(studentEmail=username).exists or Admin.objects.filter(email=username).exists():

            if "@tut4life.ac.za" in username:

                try:
                    stud = Student.objects.all().get(studentEmail=username)
                    if stud.password == password:
                        return render(request,"home/home.html")
                    else:
                        messages.error(request, "Inccorect Username / Password!")
                        return redirect("/login")

                except:
                    messages.error(request, "Inccorect Username / Password!")
                    return redirect("/login")

            elif "@mebhub.ac.za" in username:
                try:

                    admin = Admin.objects.all().get(email=username)

                    if admin.password == password:
                        return HttpResponse(f"Welcome Administrator {admin.name}")
                    else:
                        messages.error(request, "Inccorect Username / Password!")
                        return redirect("/login")
                except:
                    messages.error(request, "Incorrect Username / Password!")
                    return redirect('/login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('/login')
    else:
        return render(request, "login/login.html")


def register(request):
    if request.method == 'POST':
        student_no = request.POST['student_no']
        name = request.POST['name']
        surname = request.POST['surname']
        student_email = request.POST['student_email']
        password = request.POST['password']
        password_confirmation = request.POST['confirm_password']

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
            messages.error(request,"student not registerd on tut")
            return redirect('/login/register')

    else:
        return render(request, "login/register.html")


def admin(request):
    return render(request, "login/admin.html")
