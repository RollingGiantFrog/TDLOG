# -*- coding: utf-8 -*-
from operator import itemgetter
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils import timezone

from .models import Recipe, Ingredient, Cook_information, Instructions
# Create your views here.
class IndexView(generic.ListView):
    template_name = "fridgeApp/index.html"
    context_object_name = 'list_recipe'
    
    def get_queryset(self):
        return Recipe.objects.all()
        
def contact(request):
    return(render(request, 'fridgeApp/contact.html', {}))

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
        recipeTypeLength = len(recipeType)
        
        recipes = []        
            
        for text in form.fields:
            if form.cleaned_data[text]:
                for i in Ingredient.objects.all():
                    ingredient_text = normalize(i.ingredient_text)
                    if ingredient_text == text or ingredient_text + 's' == text or ingredient_text[:len(ingredient_text)-1] == text:
                        category = normalize(i.recipe.category)
                        length = min(len(category),recipeTypeLength)
                        if (recipeType[:length] == category[:length]) and not i.recipe in recipes:
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
    
class AddRecipeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AddRecipeForm, self).__init__(*args, **kwargs)
        self.fields['recipe_text'] = forms.CharField(label = "Nom de la recette ")
        self.fields['category'] = forms.ChoiceField( (("entree", "Entrée"), ("plat", "Plat"), ("dessert", "Dessert")), label = "Catégorie" )
        
class AddIngredientForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AddIngredientForm, self).__init__(*args, **kwargs)
        self.fields['ingredient_text'] = forms.CharField(label = "Nom de l'ingrédient ")
        self.fields['quantity'] = forms.IntegerField(label = "Quantitée ")
        self.fields['unit'] = forms.CharField(label = "Unité ")
        self.fields['category'] = forms.ChoiceField( (  ("Légume", "Légume"), 
                                                        ("Produit laitier", "Produit laitier"),
                                                        ("Condiment", "Condiment"),
                                                        ("Fruit", "Fruit"),
                                                        ("Féculent", "Féculent"),
                                                        ("Viande ou Poisson", "Viande ou Poisson"),
                                                        ("Autre", "Autre")
                                                            ), label = "Catégorie"  )

class AddInformationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AddInformationForm, self).__init__(*args, **kwargs)
        self.fields['information_text'] = forms.CharField(label = "Information")
        self.fields['value'] = forms.FloatField(label = "Valeur")
        self.fields['value_unit'] = forms.CharField(label = "Unité de la valeur")
        
class AddInstructionsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AddInstructionsForm, self).__init__(*args, **kwargs)
        self.fields['instructions_text'] = forms.CharField(widget=forms.Textarea, label = "Instructions")
        
def addDone(request):
    recipeForm = AddRecipeForm(request.POST)
    
    ingredientForm = AddIngredientForm()
    # Création du formset avec une seule itération : extra=1
    ingredientForm = forms.formset_factory(AddIngredientForm,extra=1)   
    # Récupération du formulaire géré par le mécanisme formset
    ingredientFormset = ingredientForm(request.POST)
    
    informationsForm = AddInformationForm()
    informationForm = forms.formset_factory(AddInformationForm, extra=0)
    informationFormset = informationForm(request.POST)
    
    instructionsForm = AddInstructionsForm(request.POST)
    
    if recipeForm.is_valid() and ingredientFormset.is_valid() and informationFormset.is_valid() and instructionsForm.is_valid():
            name = str(recipeForm.cleaned_data['recipe_text'])
            category0 = str(recipeForm.cleaned_data['category'])
            pub_date = timezone.now()
            recipe = Recipe.create(name, pub_date, category0)
            try:
                recipe.save()
            except:
                print("error saving the recipe")
                
            foreignKey = recipe  

            for form in ingredientFormset:
                ingredient_text = str(form.cleaned_data['ingredient_text']).lower()
                quantity = float(form.cleaned_data['quantity'])
                unit = str(form.cleaned_data['unit']).lower()
                category = str(form.cleaned_data['category']).lower()
                ingredient = Ingredient.create(foreignKey, ingredient_text, quantity, unit, category)
                ingredient.save()
                
            for form in informationFormset:
                information_text = str(form.cleaned_data['information_text']).lower()
                value = float(form.cleaned_data['value'])
                value_unit = str(form.cleaned_data['value_unit']).lower()
                information = Cook_information.create(foreignKey, information_text, value, value_unit)
                information.save()
                
            instructions_text = str(instructionsForm.cleaned_data['instructions_text'])
            instructions = Instructions.create(foreignKey, instructions_text)
            instructions.save()
            
                

    return render(request, 'fridgeApp/addDone.html',locals())
        
def add(request):
    recipeForm = AddRecipeForm()
    
    ingredientForm = AddIngredientForm()
    #Création du formset avec une seule itération : extra=1
    ingredientForm = forms.formset_factory(AddIngredientForm,extra=1)   
    # Récupération du formulaire géré par le mécanisme formset
    ingredientFormset = ingredientForm()
    
    informationForm = AddInformationForm()
    #Création du formset avec aucune itération : extra=0
    informationForm = forms.formset_factory(AddInformationForm,extra=0)   
    # Récupération du formulaire géré par le mécanisme formset
    informationFormset = informationForm()
    
    instructionsForm = AddInstructionsForm()
    
    return render(request, 'fridgeApp/add.html', locals())
        
    