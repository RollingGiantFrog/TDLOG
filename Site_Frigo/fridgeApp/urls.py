# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'fridgeApp'

urlpatterns = [
    url(r'^$', views.home),
    url(r'^contact$', views.Contact, name='contact'),
    url(r'^recipe/(?P<recipe_id>[0-9]+)$', views.recipe, name='recipe'),
]