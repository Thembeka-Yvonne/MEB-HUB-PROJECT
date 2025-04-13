import os

from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from administration.templates.admin.events.EventForms import EventForms
from login.models import Admin, Student
from events.models import Event
from datetime import datetime, date
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.conf import settings



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

    # Uses the EventForms form (Django form) to create an event and if successful, display the success.html page.
    form = EventForms()
    if request.method == 'POST':
      form = EventForms(request.POST, request.FILES)
      if form.is_valid():
        form.save()
        return redirect('success')
      else:
        print(form.errors)
    return render(request, 'admin/events/add_event.html', {'form': form, 'admin': admin})


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

            eventID = request.GET.get('eventID')
            eventImage=request.FILES.get('eventImage', None)
            #retrieve the data in the fields and create an event object
            event = get_object_or_404(Event, event_id=eventID)


            if eventImage:
             if event.image and 'eventImage'  in request.FILES:
               old_image_path = os.path.join(settings.MEDIA_ROOT, str(event.image))
               if os.path.exists(old_image_path):
                   os.remove(old_image_path)

               event.image=eventImage

            #set the event attributes to the new values and save the updated version in the database
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

def delete_events(request):
    #same code as update_events, just in this case you are deleting a certain event
    adminID = request.GET.get("adminID")
    admin = Admin.objects.all().get(admin_id=adminID)
    events = Event.objects.all()

    if request.method == 'POST':
        event_id = request.POST.get("event_id")
        event = Event.objects.all().get(event_id=event_id)
        return redirect(f"{reverse('delete_event_page')}?eventID={event.event_id}")
    return render(request, 'admin/events/delete_events.html',{'admin': admin,'events':events})

def delete_event_page(request):
    #Katlego responsible for this part
    eventID = request.GET.get('eventID')
    event = Event.objects.get(event_id=eventID)

    if request.method=='POST':
        eventID = request.POST.get('eventID')
        event1 = Event.objects.all().get(event_id=eventID)
        event1.delete()
        return redirect('success')
    return render(request, 'admin/events/delete_event_page.html', {'event': event})

def events_home(request):
    Event.objects.filter(date__lt=date.today()).delete() #automatically delete events
    studEmail=request.GET.get("studEmail")
    student=Student.objects.get(studentEmail=studEmail)
    campusID=student.campus_id

    admins=Admin.objects.filter(campus_id_id=campusID)
    admin_ids = admins.values_list('admin_id', flat=True)

    events= Event.objects.filter(admin_id__in=admin_ids)
    events=events.order_by('date')
    return render(request, 'events/events_home.html',{'events':events})
