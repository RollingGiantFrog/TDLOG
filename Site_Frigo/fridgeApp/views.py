# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse

from .models import Recipe, Ingredient
# Create your views here.
class IndexView(generic.ListView):
    template_name = "fridgeApp/index.html"
    context_object_name = 'list_recipe'
    
    def get_queryset(self):
        return Recipe.objects.all()
        
def contact(request):
    return(render(request, 'fridgeApp/contact.html', {}))
    
def add(request):
    return(render(request, 'fridgeApp/add.html', {}))

def home(request):
    return render(request, 'fridgeApp/home.html', {})

def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk = recipe_id)
    #return HttpResponseRedirect(reverse('fridgeApp:recipe',args=(recipe.id)))
    return render(request, 'fridgeApp/recipe.html', locals())

def result(request):
    form = SearchRecipeForm(request.POST)
    if form.is_valid():
        recipes = []
        for text in form.fields:
                if form.cleaned_data[text]:
                    for i in Ingredient.objects.all().filter(ingredient_text = text):
                        if not i.recipe in recipes:
                            recipes += [i.recipe]
    
    valid_recipes = []
    for recipe in recipes:
        missing = 0
        present = 0
        for ingredient in recipe.ingredient_set.all():
            if not form.cleaned_data[ingredient.ingredient_text]:
                missing += 1
            else:
                present += 1
                
        valid_recipes += [(missing,-present,recipe)]
        # On trie par ordre de nombre d'ingrédients manquants croissant 
        # puis par nombre d'ingrédients présents décroissants
        valid_recipes.sort()
    
    return render(request, 'fridgeApp/result.html', locals())

from django import forms

class SearchRecipeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SearchRecipeForm, self).__init__(*args, **kwargs)
        # dynamic fields here ...
        for i in Ingredient.objects.all():
            self.fields[i.ingredient_text] = forms.BooleanField(help_text=i.category, required=False)
    # normal fields here ...
            
def search(request):
    form = SearchRecipeForm(request.POST or None)
    
    categories = []
    ingredients = {}
    
    for text in form.fields:
        if not form.fields[text].help_text in categories:
            categories += [form.fields[text].help_text]
            ingredients[form.fields[text].help_text] = [text]
        else:  
            ingredients[form.fields[text].help_text] += [text]
    return render(request, 'fridgeApp/search.html', locals())