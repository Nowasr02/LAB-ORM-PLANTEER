from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Plant, Review, Country
from .forms import PlantForm

# Create your views here.

def add_plant_view(request : HttpRequest):
    
    countries = Country.objects.all()
    
    # if request.method == "POST":
    #         form = PlantForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             plant = form.save(commit=False)
    #             plant.save()
    #             form.save_m2m()
    #             return redirect("main:home_view")
    # else:
    #     form = PlantForm()
    
        
    if request.method == "POST":
        
        new_plant = Plant(name = request.POST["name"], 
                        about = request.POST["about"],
                        used_for = request.POST["used_for"],
                        category = request.POST.get("category"), 
                        is_edible = request.POST.get("is_edible", "false") == "true",
                        image = request.FILES["image"],
                        created_at = request.POST["created_at"],
                        # countries = request.POST["countries"]
                        )
        
        new_plant.save()
        new_plant.countries.set(request.POST.getlist("countries"))
        return redirect('main:home_view')

    return render(request, "plants/add_plant.html", {"countries" : countries})

def all_plants_view(request : HttpRequest):
    plants = Plant.objects.all().order_by("name")
    
    category = request.GET.get('category')
    if category:
        plants = plants.filter(category = category)
        
    is_edible = request.GET.get('is_edible')
    if is_edible is not None and is_edible != "":
        if is_edible.lower() in ['1', 'true', 'yes']:
            plants = plants.filter(is_edible=True)
        elif is_edible.lower() in ['0', 'false', 'no']:
            plants = plants.filter(is_edible=False)
            
    categories = Plant.objects.values_list('category', flat=True).distinct()
    
    country = request.GET.get('country')
    if country:
        plants = plants.filter(countries__name__iexact = country)
        
    countries = Country.objects.values_list('name', flat=True).distinct()
    

        
    return render(request, "plants/all_plants.html", {
        "plants": plants,
        "categories": categories,
        "countries" : countries,
    })
    

def plant_details_view(request : HttpRequest, plant_id:int):
    plant = Plant.objects.get(pk = plant_id)
    reviews = Review.objects.filter(plant = plant)
    
    same_category = Plant.objects.filter(category = plant.category)
    same_category = same_category.exclude(pk=plant.pk)
    same_category = same_category.order_by('-created_at')[:4]
    
    return render(request, "plants/plant_details.html", {
        "plant": plant,
        "plants": same_category, 
        "reviews" : reviews
    })

def update_plant_view(request : HttpRequest, plant_id:int):
    plant = Plant.objects.get(pk = plant_id)
    
    if request.method == "POST":
        plant.name = request.POST["name"]
        plant.about = request.POST["about"]
        plant.used_for = request.POST["used_for"]   
        plant.category = request.POST.get("category") 
        plant.is_edible = request.POST["is_edible"] == "true" #converting string to boolean
        if "image" in request.FILES: 
            plant.image = request.FILES["image"]
        plant.save()
        
        return redirect("plants:plant_details_view", plant_id = plant.id)
    
    return render(request, "plants/plant_update.html", {"plant" : plant})

def delete_plant_view(request : HttpRequest, plant_id:int):
    plant = Plant.objects.get(pk = plant_id)
    plant.delete()
    return redirect('main:home_view')

def search_view(request : HttpRequest):
    
    if "search" in request.GET and len(request.GET["search"]) >= 3:
        plants = Plant.objects.filter(name__contains = request.GET["search"])
    else:
        plants = []
        
    return render(request, "plants/search.html", {"plants" : plants})


def add_review_view(request : HttpRequest, plant_id):
    
    if request.method == "POST":
        plant_object = Plant.objects.get(pk = plant_id)
        new_review = Review(plant = plant_object, name = request.POST["name"],
                            rating = request.POST["rating"],
                            comment = request.POST["comment"],
                            )
        new_review.save()
    
    return redirect('plants:plant_details_view', plant_id = plant_id)