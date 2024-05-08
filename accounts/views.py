from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login, authenticate

def registration_view(request):
    login_form = AuthenticationForm()
    signup_form = UserCreationForm()

    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                return redirect('home')  # Redirect to the home page after successful login
        elif 'signup' in request.POST:
            signup_form = UserCreationForm(request.POST)
            if signup_form.is_valid():
                username = signup_form.cleaned_data.get('username')
                password = signup_form.cleaned_data.get('password1')
                email = signup_form.cleaned_data.get('email')
                user = signup_form.save()
                user.email = email  # Update email
                user.save()
                user = authenticate(username=username, password=password)
                auth_login(request, user)
                return redirect('home')  # Redirect to the home page after successful signup

    return render(request, 'registration.html', {'login_form': login_form, 'signup_form': signup_form})
