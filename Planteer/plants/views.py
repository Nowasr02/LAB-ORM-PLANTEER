from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Plant

# Create your views here.

def add_plant_view(request : HttpRequest):

    if request.method == "POST":
        
        new_plant = Plant(name = request.POST["name"], 
                        about = request.POST["about"],
                        used_for = request.POST["used_for"],
                        category = request.POST.get("category"), 
                        is_edible = request.POST.get("is_edible", "false") == "true",
                        image = request.FILES["image"],
                        created_at = request.POST["created_at"]
                        )
        new_plant.save()
        return redirect('main:home_view')

    return render(request, "plants/add_plant.html")

def all_plants_view(request : HttpRequest):
    plants = Plant.objects.all().order_by("name")
    
    category = request.GET.get('category')
    if category:
        plants = plants.filter(category = category)
        
    is_edible = request.GET.get('is_edible')
    if is_edible:
        if is_edible.lower() in ['1', 'true', 'yes']:
            plants = plants.filter(is_edible=True)
        elif is_edible.lower() in ['0', 'false', 'no']:
            plants = plants.filter(is_edible=False)
            
    categories = Plant.objects.values_list('category', flat=True).distinct()
    
    return render(request, "plants/all_plants.html", {
        "plants": plants,
        "categories": categories,
    })

def plant_details_view(request : HttpRequest, plant_id:int):
    plant = Plant.objects.get(pk = plant_id)
    
    same_category = Plant.objects.filter(category = plant.category)
    same_category = same_category.exclude(pk=plant.pk)
    same_category = same_category.order_by('-created_at')[:4]
    
    return render(request, "plants/plant_details.html", {
        "plant": plant,
        "plants": same_category,
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
    post = Plant.objects.get(pk = plant_id)
    post.delete()
    return redirect('main:home_view')

def search_view(request : HttpRequest):
    
    if "search" in request.GET and len(request.GET["search"]) >= 3:
        plants = Plant.objects.filter(name__contains = request.GET["search"])
    else:
        plants = []
        
    return render(request, "plants/search.html", {"plants" : plants})
