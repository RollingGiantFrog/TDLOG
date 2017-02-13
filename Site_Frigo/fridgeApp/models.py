# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Recipe(models.Model):
    recipe_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')
    category = models.CharField(max_length = 200)
    #cook_time = models.FloatField()
    #rest_time = models.FloatField()
    #preparation_time = models.FloatField()
    def __str__(self):
        return self.recipe_text
    @classmethod
    def create(cls, recipe_text, pub_date, category):
        recipe = cls(recipe_text=recipe_text, pub_date=pub_date, category=category)
        return recipe

class Cook_information(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    information_text = models.CharField(max_length = 200)
    value = models.FloatField()
    value_unit = models.CharField(max_length = 30)
    def __str__(self):
        return self.information_text
    @classmethod
    def create(cls, recipe, information_text, value, value_unit):
        ingredient = cls(recipe=recipe, information_text=information_text, value=value, value_unit=value_unit)
        return ingredient
        
class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_text = models.CharField(max_length = 50)
    quantity = models.FloatField()
    unit = models.CharField(max_length = 30)
    category = models.CharField(max_length = 200)
    def __str__(self):
        return self.ingredient_text
    @classmethod
    def create(cls, recipe, ingredient_text, quantity, unit, category):
        ingredient = cls(recipe=recipe, ingredient_text=ingredient_text, quantity=quantity, unit=unit, category=category)
        return ingredient


class Instructions(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    instructions_text = models.CharField(max_length = 1500)
    def __str__(self):
        return "Consignes"
    @classmethod
    def create(cls, recipe, instructions_text):
        instructions = cls(recipe=recipe, instructions_text=instructions_text)
        return instructions