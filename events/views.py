from django.shortcuts import render

# Create your views here.
def add_event(request):
    return render(request, 'events/add_event.html')

def update_event_page(request):
    return render(request, 'events/update_event_page.html')

def update_events(request):
    return render(request, 'events/update_events.html')

def delete_event(request):
    return render(request, 'events/delete_event.html')


