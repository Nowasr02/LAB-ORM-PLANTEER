from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
# from plants.models import Plant
from .models import Country
from .forms import CountryForm

# Create your views here.

def add_country(request:HttpRequest):

    if request.method == "POST":
        #addin a new plant in database
        country_form = CountryForm(request.POST, request.FILES)
        if country_form.is_valid():
            country_form.save()
        else:
            print(country_form.errors)

        return redirect("countries:countries_view")

    return render(request, "countries/add_country.html")


   
#for all countries
def countries_view(request : HttpRequest):
    countries = Country.objects.all()[:3]
    
    return render(request, "countries/countries.html", {"countries" : countries})


#for one country based on id
def country_view(request : HttpRequest, country_id):
    country = Country.objects.get(id = country_id)
    
    return render(request, "countries/country.html", {"country" : country})