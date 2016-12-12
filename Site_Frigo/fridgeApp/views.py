# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views import generic

from .models import Recipe
# Create your views here.
class IndexView(generic.ListView):
    template_name = "fridgeApp/index.html"
    context_object_name = 'list_recipe'
    
    def get_queryset(self):
        return Recipe.objects.all()
        
def Contact(request):
    return(render(request, 'fridgeApp/contact.html'))