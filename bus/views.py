from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Bus_schedule,ScheduleCode
from .forms import ApplicationConfirmationForm
from login.models import Student
import pytesseract
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageOps
import io

# Create your views here.s
def home(request):
    list = ScheduleCode.objects.all()
    return render(request,"buses/home.html",{
        "list": list
    })

def view_schedule(request,schedule_code):
    list = Bus_schedule.objects.filter(schedule_code=schedule_code)

    return render(request,"buses/view_schedule.html",{
        "list": list
    })


def upload_img_and_check(request):
    if request.method == 'POST':
        form = ApplicationConfirmationForm(request.POST, request.FILES)
        if form.is_valid():
            if 'document' not in request.FILES:
                messages.error(request, "No file uploaded")
                return redirect('view_status')

            try:
                document = request.FILES['document']
                image = Image.open(io.BytesIO(document.read())).convert('RGB')

                # Convert PIL to OpenCV format
                open_cv_image = np.array(image)
                image_cv = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

                # Preprocessing improvements
                # 1. Convert to grayscale
                gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

                # 2. Apply Gaussian blur to reduce noise
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)

                # 3. Use different thresholding approach
                # Try both adaptive and simple thresholding and pick the better result
                thresh_adaptive = cv2.adaptiveThreshold(blurred, 255,
                                                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 10)

                _, thresh_simple = cv2.threshold(blurred, 0, 255,
                                                 cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # 4. Try both thresholding methods and see which gives better results
                custom_config = r'--oem 3 --psm 6'
                text_adaptive = pytesseract.image_to_string(thresh_adaptive, config=custom_config)
                text_simple = pytesseract.image_to_string(thresh_simple, config=custom_config)

                # Choose the version with more valid words
                extracted_text = text_adaptive if (
                            len(text_adaptive.split()) > len(text_simple.split())) else text_simple

                # Alternative approach if both fail - try without thresholding
                if len(extracted_text.strip()) < 20:  # If we got very little text
                    extracted_text = pytesseract.image_to_string(gray, config=custom_config)

                print("Extracted text:", extracted_text)  # For debugging

                expected_texts = [
                    "good day student",
                    "Please note that your student bus application for the academic year 2025 was approved and you may now proceed to make your student card",
                    "transport department"
                ]

                studentNum = request.session.get('student_number')
                student = Student.objects.get(studentNumber=studentNum)

                # More flexible text matching
                extracted_lower = extracted_text.lower()
                matches = sum(1 for expected in expected_texts if expected.lower() in extracted_lower)

                if matches >= 2:  # Require at least 2 out of 3 expected phrases
                    student.uses_bus = True
                    student.save()
                    messages.success(request, "Verification successful!")
                else:
                    messages.error(request, "Verification unsuccessful! Could not find required text in the image.")

            except Exception as e:
                messages.error(request, f"Error processing image: {str(e)}")
                return redirect('view_status')

            return redirect('view_status')

    return redirect('view_status')

def view_status(request):
    studentNum = request.session.get('student_number')
    student = Student.objects.all().get(studentNumber=studentNum)
    initials = f"{student.name[0].upper()}{student.surname[0].upper()}"
    uses_bus = student.uses_bus
    context = {
        "initials": initials,
        "status": uses_bus,
        "confirmation_form": ApplicationConfirmationForm()
    }
    return render(request, "buses/view_status.html", context)