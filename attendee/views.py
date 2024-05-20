from django.shortcuts import render,get_object_or_404,redirect
from admin_panel.models import Event,EventCategory
from django.core.mail import send_mail
from django.utils import timezone
from .forms import EventOrganizerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.views import View
from django.conf import settings
from .models import Ticket
from admin_panel.models import Event as AdminPanelEvent
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from PIL import Image 
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4



def home(request):
    latest_events = Event.objects.filter(date_time__gte=timezone.now()).order_by('-date_time')[:4]
    active_link = 'home'
    context = {
        'latest_events': latest_events,
        'active_link': active_link,
    }
    return render(request, 'home.html', context)

def event_organizer_form(request):
    if request.method == 'POST':
        form = EventOrganizerForm(request.POST)
        if form.is_valid():
            # Get form data
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            college_name = form.cleaned_data['college_name']
            department = form.cleaned_data['department']
            additional_notes = form.cleaned_data['additional_notes']
            
            # Send email to admin
            send_mail(
                'New Event Organizer Request',
                f'Name: {full_name}\nEmail: {email}\nPhone: {phone_number}\nCollege: {college_name}\nDepartment: {department}\nNotes: {additional_notes}',
                'your_email@example.com',
                ['admin@example.com'],
                fail_silently=False,
            )
            # Redirect to a success page or show a success message
            return render(request, 'success.html')
    else:
        form = EventOrganizerForm()
    return render(request, 'create_event_organizer.html', {'form': form})

def events_list(request):
    all_events = Event.objects.all()  
    categories = EventCategory.objects.all()
    active_link = 'events'
    context = {
        'all_events': all_events,
        'categories': categories,
        'active_link': active_link,
    }
    return render(request, 'events_list.html', context)

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    active_link = 'events'

    context = {
        'event': event,
        'active_link': active_link,
    }
    return render(request, 'event_detail.html', context)


def generate_pdf(request):
    # Retrieve form data from request
    name = request.POST.get('name')
    gender = request.POST.get('gender')
    phone_number = request.POST.get('phone_number')
    user_role = request.POST.get('user_role')
    event_name = request.POST.get('event_name')
    event_price = request.POST.get('event_price')
    total_price = request.POST.get('total_price')
    quantity = request.POST.get('quantity')

    # Log the retrieved form fields for debugging
    print(f"Name: {name}")
    print(f"Gender: {gender}")
    print(f"Phone Number: {phone_number}")
    print(f"User Role: {user_role}")
    print(f"Event Name: {event_name}")
    print(f"Event Price: {event_price}")
    print(f"Total Price: {total_price}")
    print(f"Quantity: {quantity}")

    # Error checking for form fields
    if not name or not gender or not phone_number or not user_role or not event_name or not event_price or not total_price or not quantity:
        return HttpResponse("Missing form fields", status=400)

    try:
        event_price = float(event_price.replace('₹', '').strip())
        total_price = float(total_price.replace('₹', '').strip())
        quantity = int(quantity)
    except ValueError:
        return HttpResponse("Invalid form field values", status=400)

    # Generate QR Codes for each attendee
    qr_codes = []
    for i in range(quantity):
        attendee_data = f"Name: {name}\nGender: {gender}\nPhone Number: {phone_number}\nUser Role: {user_role}\nEvent Name: {event_name}\nEvent Price: {event_price}\nTotal Price: {total_price}\nAttendee: {i+1}"
        qr = qrcode.make(attendee_data)
        qr_code_buffer = BytesIO()
        qr.save(qr_code_buffer, format="PNG")
        qr_code_buffer.seek(0)
        qr_codes.append(qr_code_buffer)

    # Generate PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="registration_details.pdf"'
    
    # Create PDF content
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Add form details to PDF
    y_position = 750
    p.drawString(100, y_position, f"Name: {name}")
    y_position -= 20
    p.drawString(100, y_position, f"Gender: {gender}")
    y_position -= 20
    p.drawString(100, y_position, f"Phone Number: {phone_number}")
    y_position -= 20
    p.drawString(100, y_position, f"User Role: {user_role}")
    y_position -= 20
    p.drawString(100, y_position, f"Event Name: {event_name}")
    y_position -= 20
    p.drawString(100, y_position, f"Event Price: {event_price}")
    y_position -= 20
    p.drawString(100, y_position, f"Total Price: {total_price}")

    # Add QR codes to PDF
    y_position -= 40  # Add some space before the QR codes
    for qr_code in qr_codes:
        qr_code.seek(0)
        pil_image = Image.open(qr_code)
        qr_code_image = BytesIO()
        pil_image.save(qr_code_image, format='PNG')
        qr_code_image.seek(0)
        p.drawInlineImage(Image.open(qr_code_image), 100, y_position, width=100, height=100)
        y_position -= 120  # Adjust the spacing between QR codes

    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

def registration_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('attendee:events_list') 
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})

