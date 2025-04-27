from django.db import models

# Create your models here.


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    cooking_time = models.IntegerField(help_text="Time in minutes")
    ingredients = models.TextField(help_text="Comma-separated list of ingredients")
    description = models.TextField(blank=True)  # Optional small description
    difficulty = models.CharField(max_length=10)
    pic = models.ImageField(upload_to='recipes', default='no_picture.png')


    def __str__(self):
        return self.name