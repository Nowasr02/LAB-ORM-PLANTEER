from django.shortcuts import render
from django.http import HttpRequest
from plants.models import Plant

# Create your views here.

def home_view(request : HttpRequest):
    
    if request.user.is_authenticated:
        print(request.user.username)
    else:
        print("User is not logged in")
    
    plants = Plant.objects.order_by('-created_at')[:4]
    return render(request, "main/home.html", {"plants" : plants})