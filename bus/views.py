from django.shortcuts import render
from .models import Bus_schedule,ScheduleCode
from .models import Bus_Stats
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# Create your views here.s
def home(request):
    list = ScheduleCode.objects.all()
    return render(request,"buses/home.html",{
        "list": list
    })

def view_schedule(request,schedule_code):

    if request.method == 'POST':
        
        code = request.POST['code']
        list = Bus_schedule.objects.filter(schedule_code=code)
        
        #Creating a response object with the appropriate content type for PDFs
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="bus_schedule.pdf"'
        
        #Creating a pdf canvas object
        p = canvas.Canvas(response,pagesize=letter)
        width, height = letter
        
        # Creating Title for the report
        p.setFont("Helvetica-Bold", 16)
        p.drawString(200, height - 40, "Bus Schedule")
        
        # Creating the font for the table headers and content
        p.setFont("Helvetica-Bold", 12) 
        
        # Draw table header
        p.drawString(30, height - 80, "Code")
        p.drawString(120, height - 80, "Departure")
        p.drawString(210, height - 80, "Destination")
        p.drawString(300, height - 80, "Departure-Time")
        p.drawString(390, height - 80, "Arrival-Time")
        p.drawString(480, height - 80, "Duration")
        
        # Set the font for the table content
        p.setFont("Helvetica", 10)
        
        # Start position for the table rows
        y_position = height - 100
        
        for schedule in list:
            
            p.drawString(30, y_position, code)
            p.drawString(120, y_position, schedule.departure)
            p.drawString(210, y_position, schedule.destination)
            p.drawString(300, y_position, schedule.departure_time.strftime('%H:%M'))
            p.drawString(390, y_position, schedule.arrival_time.strftime('%H:%M'))
            p.drawString(480, y_position, str(schedule.duration))
            y_position -= 20  # Move to the next row

            # Add a page break if the content goes beyond the page
            if y_position < 40:
                p.showPage()  # Start a new page
                p.setFont("Helvetica-Bold", 12)
                p.drawString(30, y_position, code)
                p.drawString(120, y_position, schedule.departure)
                p.drawString(210, y_position, schedule.destination)
                p.drawString(300, y_position, schedule.departure_time.strftime('%H:%M'))
                p.drawString(390, y_position, schedule.arrival_time.strftime('%H:%M'))
                p.drawString(480, y_position, str(schedule.duration))
                p.setFont("Helvetica", 10)
                y_position = height - 60  # Reset y_position for the new page
        
        # Finalize the PDF document
        p.showPage()
        p.save()
        
        return response

    list = Bus_schedule.objects.filter(schedule_code=schedule_code)
    
    schedule = ScheduleCode(schedule_code=schedule_code)
    stats = Bus_Stats(schedule_code=schedule)
    stats.save()
    
    return render(request,"buses/view_schedule.html",{
        "list": list,
        "schedule_code": schedule_code
    })


