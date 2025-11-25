from django.db import models

# Create your models here.

class Country(models.Model):
    
    name = models.CharField(max_length = 128, unique = True)
    flag = models.ImageField(upload_to="images/")
    
    def __str__(self) -> str:
        return self.name