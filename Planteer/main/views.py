from django.shortcuts import render, redirect
from django.http import HttpRequest
from plants.models import Plant
from .models import Contact
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages


# Create your views here.

def home_view(request : HttpRequest):
    
    if request.user.is_authenticated:
        print(request.user.username)
    else:
        print("User is not logged in")
    
    plants = Plant.objects.order_by('-created_at')[:4]
    return render(request, "main/home.html", {"plants" : plants})

def contact_view(request:HttpRequest):
    
    if request.method == "POST":
        contact = Contact(
            name = request.POST["name"],
            email = request.POST["email"],
            message = request.POST["message"]
        )
        contact.save()
        
        #send confirmation email
        content_html = render_to_string("main/mail/confirmation.html")
        send_to = contact.email
        email_message = EmailMessage("confirmation", content_html, settings.EMAIL_HOST_USER, [send_to])
        email_message.content_subtype = "html"
        # email_message.connection = email_message.get_connection(True)
        email_message.send()
        
        messages.success(request, "We recieved your successfully", "alert-success")

    return render(request, 'main/contact.html' )