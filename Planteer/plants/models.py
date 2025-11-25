from django.db import models
from countries.models import Country

# Create your models here.
    
class Plant(models.Model):
    class Category(models.TextChoices):
        ORNAMENTAL = 'ornamental'
        INDOOR = 'indoor'
        OUTDOOR = 'outdoor'
        FLOWERING = 'flowering'
    
    name = models.CharField(max_length = 2048)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="images/")
    category = models.CharField(
        max_length = 10,
        choices = Category.choices,
    )
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    countries = models.ManyToManyField(Country)
    
    def __str__(self):
        return self.name

class Review(models.Model):
    plant = models.ForeignKey(Plant, on_delete = models.CASCADE)
    
    name = models.CharField(max_length = 1024)
    rating = models.SmallIntegerField()
    comment = models.TextField()
    review_date = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f"{self.name} on {self.plant.name}"
    
    

    