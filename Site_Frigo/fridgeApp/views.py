# -*- coding: utf-8 -*-
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
        
def Contact(request):
    return(render(request, 'fridgeApp/contact.html'))

def home(request):
    return render(request, 'fridgeApp/home.html', {})

def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk = recipe_id)
    #return HttpResponseRedirect(reverse('fridgeApp:recipe',args=(recipe.id)))
    return render(request, 'fridgeApp/recipe.html', locals())



from django import forms

class SearchRecipeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SearchRecipeForm, self).__init__(*args, **kwargs)
        # dynamic fields here ...
        for i in Ingredient.objects.all():
            self.fields[i.ingredient_text] = forms.BooleanField(help_text="\n", required=False)
    # normal fields here ...
            
def search(request):
    form = SearchRecipeForm(request.POST or None)
    return render(request, 'fridgeApp/search.html', locals())