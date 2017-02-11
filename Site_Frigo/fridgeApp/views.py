# -*- coding: utf-8 -*-
from operator import itemgetter
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


accents = [['é','è','ê'],['ù','û'],['à','â'],['î'],['ô']]
vowels = ['e','u','a','i','o']

def removeAccents(s):
    for i in range(len(s)):
        c = s[i]
        for k in range(len(accents)):
            if c in accents[k]:
                s = s[:i] + vowels[k] + s[i+1:]
                break
    return s

def normalize(s):
    return removeAccents(s.lower())
    
def compare(s1,s2):
    s1 = s1.lower()
    s2 = s2.lower()
    
    s1 = removeAccents(s1)
    s2 = removeAccents(s2)
    
    return s1 == s2

def result(request):
    form = SearchRecipeForm(request.POST)
    if form.is_valid():
        recipeType = ""
        if form.cleaned_data[normalize("entree")]:
            recipeType = normalize("entree")
        if form.cleaned_data[normalize("plat")]:
            recipeType = normalize("plat")
        if form.cleaned_data[normalize("dessert")]:
            recipeType = normalize("dessert")
            
        recipes = []        
            
        for text in form.fields:
            if form.cleaned_data[text]:
                for i in Ingredient.objects.all():
                    ingredient_text = normalize(i.ingredient_text)
                    if ingredient_text == text or ingredient_text + 's' == text or ingredient_text[:len(ingredient_text)-1] == text:
                        if (recipeType == normalize(i.recipe.category)[len(recipeType)]) and not i.recipe in recipes:
                            recipes += [i.recipe]
    
    valid_recipes = []
    for recipe in recipes:
        missing = 0
        present = 0
        for ingredient in recipe.ingredient_set.all():
            text = normalize(ingredient.ingredient_text)
            if (not text in form.cleaned_data or not form.cleaned_data[text]) and (not text + 's' in form.cleaned_data or not form.cleaned_data[text + 's']) and (not text[:len(text)-1] in form.cleaned_data or not form.cleaned_data[text[:len(text)-1]]):
                missing += 1
            else:
                present += 1
        valid_recipes += [(missing,-present,recipe)]
        # On trie par ordre de nombre d'ingrédients manquants croissant 
        # puis par nombre d'ingrédients présents décroissants
        valid_recipes.sort(key = itemgetter(0,1))

    length=len(valid_recipes)
    return render(request, 'fridgeApp/result.html', locals())

from django import forms

class SearchRecipeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SearchRecipeForm, self).__init__(*args, **kwargs)
        # dynamic fields here ...
        ingredient_texts = {}
        for i in Ingredient.objects.all():
            text = normalize(i.ingredient_text)
            if not text in ingredient_texts and not text[:len(text)-1] in ingredient_texts and not text + 's' in ingredient_texts:
                self.fields[text] = forms.BooleanField(help_text=i.category, required=False)
                ingredient_texts[text] = True
                
        self.fields[normalize("entree")] = forms.BooleanField(required=False)
        self.fields[normalize("plat")] = forms.BooleanField(required=False)
        self.fields[normalize("dessert")] = forms.BooleanField(required=False)
        
        #for j in Recipe.objects.all():
           #self.fields[j.category] = forms.BooleanField(help_text="", required=False)
        # normal fields here ...
            
def search(request):
    form = SearchRecipeForm(request.POST or None)
    
    categories = []
    ingredients = {}
    
    for text in form.fields:
        if form.fields[text].help_text != "":
            if not form.fields[text].help_text in categories:
                categories += [form.fields[text].help_text]
                ingredients[form.fields[text].help_text] = [text]
            else:
                ingredients[form.fields[text].help_text] += [text]

    categories.sort(key=lambda v: v.upper())

    for category in categories:
        ingredients[category].sort(key=lambda v: v.upper())
        print (ingredients[category])
    
    return render(request, 'fridgeApp/search.html', locals())
    
    