from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import CustomUser

def registration_view(request):
    if request.method == 'POST':
        if 'signup' in request.POST:
            # Handle user registration
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password == confirm_password:
                try:
                    user = CustomUser.objects.create_user(username=username, email=email, password=password)
                    user.user_type = 'attendee'  # Set the default user type to 'attendee'
                    user.save()
                    # Redirect to the login page after successful signup
                    return redirect('login')
                except Exception as e:
                    error_message = str(e)
                    return render(request, 'registration.html', {'error_message': error_message})
            else:
                error_message = "Passwords do not match"
                return render(request,'registration.html', {'error_message': error_message})
        else:
            # Handle user login
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Check user type and redirect to the appropriate dashboard
                if user.user_type == 'admin':
                    return redirect('admin_panel:dashboard')
                elif user.user_type == 'organizer':
                    return redirect('event_organizer:dashboard')
                else:
                    return redirect('attendee:home')
            else:
                error_message = "Invalid login credentials"
                return render(request, 'registration.html', {'error_message': error_message})
    return render(request, 'registration.html')
