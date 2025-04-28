import os
from contextlib import nullcontext

from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from administration.templates.admin.events.EventForms import EventForms
from login.models import Admin, Student
from events.models import Event
from datetime import datetime, date
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# Create your views here.
def add_event(request):
    adminEmail = request.GET.get("adminEmail")
    admin = Admin.objects.select_related('campus_id').get(email=adminEmail)

    # 'select_related' obtains all data at one time through a multi-table join Association
    # We have two tables that are related through foreign key 'campus_id', so basically what
    # is that the data related to the Admin in the campus table is stored as an attribute in the
    # Admin table with the attribute name "campus_id", so to access the information of the campus
    # the Admin is related to you have to access it through the foreign key linking the two tables.
    # We make use of select_related to retrieve the information of a specific Admin object which has
    # campus_id foreign key which points to the Campus model.

    # instead of using Django form for the input values of adding events, I manually created the form.  Reason is django form does not serve binary files
    if request.method == 'POST':
        description = request.POST.get('description')
        date = request.POST.get('date')
        location = request.POST.get('location')
        admin_id = request.POST.get('admin_id')
        image_file =request.FILES.get('image')
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']

        s_time = datetime.strptime(start_time, '%H:%M')
        e_time = datetime.strptime(end_time, '%H:%M')
        image_data=image_file.read() #read binary file so it can be stored in the database

        if image_file:
            event = Event(
                description=description,
                date=date,
                location=location,
                admin_id_id=admin_id,
                image=image_data,
                start_time=s_time.time(),
                end_time=e_time.time()
            )
            event.save()
        return redirect('success')

    return render(request, 'admin/events/add_event.html', { 'admin': admin})


def success(request):
  # page displayed if event is added successfully
  return render(request, 'admin/events/success.html')


def update_event_page(request):
    #this is the page which admin uses to update events.
    if request.method=='POST':
        try:
            dateStr= request.POST.get("date")
            date_obj=datetime.strptime(dateStr,"%B %d, %Y").date()

            location = request.POST.get("location")
            description=request.POST.get("description")

            start_time = request.POST['start_time']
            end_time = request.POST['end_time']


            eventID = request.GET.get('eventID')
            eventImage=request.FILES.get('eventImage')
            #retrieve the data in the fields and create an event object
            event = get_object_or_404(Event, event_id=eventID)

            # set the event attributes to the new values and save the updated version in the database
            if eventImage:
                event.image = eventImage.read()  #test if image is updated or not

            if start_time:
                s_time = datetime.strptime(start_time, '%H:%M')
                event.start_time = s_time.time()

            if end_time:
                e_time = datetime.strptime(end_time, '%H:%M')
                event.end_time = e_time.time()


            event.date=date_obj
            event.location=location
            event.description=description

            event.save()

            messages.success(request, "Account Updated")
            return redirect(f"{reverse('update_event_page')}?eventID={event.event_id}")
        except ValueError:
            return HttpResponseBadRequest("Invalid date format. Please use 'Nov. 25, 2025' ") #handling exception of wrong date format

    #retrieve eventID from the url (GET method) and create event object which you will pass to the template to
    #display relevant information to update.
    eventID = request.GET.get('eventID')
    event = Event.objects.get(event_id=eventID)
    if not event:
                messages.error(request, "Event not found!")
                return redirect("/update_events")

    return render(request, 'admin/events/update_event_page.html',{'event':event})

def update_events(request):
    #recieves the adminID from the URL which is passed from the admin.html page and you retrieve the events posted
    #by that specfic admin, pass the list of events to the template to display so admin can choose which event to update,
    #once event is select, redirect to update_event_page to allow admin to update the event details
    adminID=request.GET.get("adminID")
    admin=Admin.objects.all().get(admin_id=adminID)
    events=Event.objects.all()

    if request.method=='POST':
        event_id=request.POST.get("event_id")
        event=Event.objects.all().get(event_id=event_id)
        return redirect(f"{reverse('update_event_page')}?eventID={event.event_id}")
    return render(request, 'admin/events/update_events.html', {'admin': admin,'events':events})


def events_home(request):
    Event.objects.filter(date__lt=date.today()).delete() #automatically delete events
    studEmail=request.GET.get("studEmail")
    student=Student.objects.get(studentEmail=studEmail)


    events= Event.objects.all()
    events=events.order_by('date')
    return render(request, 'events/events_home.html',{'events':events})

def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def rsvp_event(request):
    eventID=request.GET.get("eventID")
    event=Event.objects.get(event_id=eventID)

    time = event.start_time.strftime('%H:%M')+"-"+event.end_time.strftime('%H:%M')


    if request.method=='POST':
        event_id = request.POST.get("eventID")
        event = Event.objects.all().get(event_id=event_id)
        student_no = request.POST['studentNo']
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        time = event.start_time.strftime('%H:%M') + "-" + event.end_time.strftime('%H:%M')

        if is_valid_email(email): #check if the email is valid
            messages.success(request, "RSVP Successful")

            if event.count is None:
                event.count = 1
            else:
                event.count = event.count + 1 #increment event count everytime a student decides to RSVP that certain event
            event.save()

            return redirect(f"{reverse('rsvp_event')}?eventID={event.event_id}")
        else:
            messages.success(request, "Invalid email!! Try again")
            return redirect(f"{reverse('rsvp_event')}?eventID={event.event_id}")

    return render(request,'events/rsvp_event.html',{'event':event,'time':time})

def serve_image(request,id): #serve the image from the database as image, converting it from binary to image
    event = Event.objects.get(event_id=id)
    return HttpResponse(event.image, content_type="image/jpeg")  # Or png
