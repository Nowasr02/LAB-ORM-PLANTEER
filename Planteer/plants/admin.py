from django.contrib import admin
from .models import Plant, Review, Country

# Register your models here.

class PlantAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    
    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "plant", "rating")
    list_filter = ("rating",)
    
admin.site.register(Plant, PlantAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Country)


