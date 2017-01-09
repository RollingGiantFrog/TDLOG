# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Recipe(models.Model):
    recipe_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')
    #cook_time = models.FloatField()
    #rest_time = models.FloatField()
    #preparation_time = models.FloatField()
    def __str__(self):
        return self.recipe_text
    
class Cook_information(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    information_text = models.CharField(max_length = 200)
    value = models.FloatField()
    value_unit = models.CharField(max_length = 30)
    def __str__(self):
        return self.information_text
        
class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_text = models.CharField(max_length = 200)
    quantity = models.FloatField()
    unit = models.CharField(max_length = 30)
    def __str__(self):
        return self.ingredient_text

class Instructions (models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    instructions_text = models.CharField(max_length = 1500)
    def __str__(self):
        return "Consignes"