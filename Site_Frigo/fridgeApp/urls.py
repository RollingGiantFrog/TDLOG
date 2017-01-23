# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'fridgeApp'

urlpatterns = [
    url(r'^home$', views.home, name='home'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^recipe/(?P<recipe_id>[0-9]+)$', views.recipe, name='recipe'),
    url(r'^search/$', views.search, name='search'),
    url(r'^add$', views.add, name='add'),
]