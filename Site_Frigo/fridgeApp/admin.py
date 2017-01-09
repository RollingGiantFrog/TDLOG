# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Recipe, Ingredient, Cook_information , Instructions
# Register your models here.
class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1
    
class CookInline(admin.TabularInline):
    model = Cook_information
    extra = 1

class InstructionsInLine(admin.TabularInline):
    model = Instructions
    extra = 1    
    
class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields':['recipe_text']}),
        ('Date information',{'fields':['pub_date'], 'classes':['collapse']}),
#        ('Cooking information', {'fields':['cook_time','rest_time',
#'preparation_time'], 'classes':['collapse']}),
    ]
    inlines = [IngredientInline, CookInline
               , InstructionsInLine
               ]

admin.site.register(Recipe, RecipeAdmin)