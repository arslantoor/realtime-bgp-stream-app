from django.contrib import admin
from django.urls import path
from .views import *
from django.urls import re_path
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('filter/<int:filter_by>/', filter,name="filter"),
    path('ripe/', RipeView.as_view(), name='ripe'),
    path('route/', RouteView.as_view(), name='route'),
    path('documentation/', Documentations.as_view(), name='documentation'),
    path('install/', InstallView.as_view(), name='install'),
    path('contact/', ContactView.as_view(), name='contact'),
    
]