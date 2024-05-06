from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def admin_dashboard(request):
    return render(request, 'index.html')