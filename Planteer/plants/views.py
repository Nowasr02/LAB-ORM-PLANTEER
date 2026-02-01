from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Plant, Review, Country
from .forms import PlantForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q, F, Count, Avg


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
                        watering = request.POST.get("watering"),
                        # countries = request.POST["countries"]
                        )
        
        
        new_plant.save()
        messages.success(request, "Added plant successfully", "alert-success")
        new_plant.countries.set(request.POST.getlist("countries"))
        return redirect('main:home_view')

        
    return render(request, "plants/add_plant.html", {"countries" : countries})

def all_plants_view(request : HttpRequest):
    plants = Plant.objects.all().order_by("name")
    
    #filter by category
    category = request.GET.get('category')
    if category:
        plants = plants.filter(category = category)
        
    #filter by is_edible
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

    plants = plants.annotate(reviews_count = Count("review"))
    
    #pagination      
    page_num = request.GET.get("page", 1)
    paginator = Paginator(plants, 6)
    plants_page = paginator.get_page(page_num)

        
    return render(request, "plants/all_plants.html", {
        "plants": plants_page,
        "categories": categories,
        "countries" : countries,
        "paginator": paginator,
    })
    

def plant_details_view(request : HttpRequest, plant_id:int):
    plant = Plant.objects.get(pk = plant_id)
    reviews = Review.objects.filter(plant = plant)
    
    avg = reviews.aggregate(Avg("rating"))
    print(avg)
    
    same_category = Plant.objects.filter(category = plant.category)
    same_category = same_category.exclude(pk=plant.pk)
    same_category = same_category.order_by('-created_at')[:4]
    
    return render(request, "plants/plant_details.html", {
        "plant": plant,
        "plants": same_category, 
        "reviews" : reviews,
        "average_rating" : avg["rating__avg"]
    })

def update_plant_view(request : HttpRequest, plant_id:int):
    plant = Plant.objects.get(pk = plant_id)
    countries = Country.objects.all()
    
    if request.method == "POST":
        plant.name = request.POST["name"]
        plant.about = request.POST["about"]
        plant.used_for = request.POST["used_for"]   
        plant.category = request.POST.get("category") 
        plant.watering = request.POST.get("watering")
        plant.is_edible = request.POST["is_edible"] == "true" #converting string to boolean
        if "image" in request.FILES: 
            plant.image = request.FILES["image"]
        plant.save()
        
        selected_country_ids = request.POST.getlist("countries")
        selected_country_ids = [int(cid) for cid in selected_country_ids if cid]
        valid_countries = Country.objects.filter(id__in=selected_country_ids)
        plant.countries.set(valid_countries)
        plant.save()

        
        return redirect("plants:plant_details_view", plant_id = plant.id)
    
    return render(request, "plants/plant_update.html", {"plant" : plant, "countries" : countries})


def delete_plant_view(request : HttpRequest, plant_id:int):
    
    try:
        plant = Plant.objects.get(pk = plant_id)
        plant.delete()
        messages.success(request, "Deleted plant successfully", "alert-success")
        
    except Exception as e:
        print(e)
        messages.error(request, "Couldn't delete plant", "alert-danger")
        
    return redirect('main:home_view')

def search_view(request : HttpRequest):
    
    if "search" in request.GET and len(request.GET["search"]) >= 3:
        plants = Plant.objects.filter(name__contains = request.GET["search"])
    else:
        plants = []
        
    return render(request, "plants/search.html", {"plants" : plants})


def add_review_view(request : HttpRequest, plant_id):
    
    if not request.user.is_authenticated:
        messages.error(request, "Only registered users can add comments")
        return redirect("accounts:sign_in")
    
    if request.method == "POST":
        plant_object = Plant.objects.get(pk = plant_id)
        new_review = Review(plant = plant_object, 
                            user = request.user,
                            rating = request.POST["rating"],
                            comment = request.POST["comment"],
                            )
        new_review.save()
    
        messages.success(request, "Comment added successfully", "alert-success")
    
    return redirect('plants:plant_details_view', plant_id = plant_id)