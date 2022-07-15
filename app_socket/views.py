import json
import calendar
from django.shortcuts import render
from django.views import View
import requests


# Create your views here.
class Home(View):
    def get(self, request):
        return render(request, 'home/index.html')

class RipeView(View):
    def get(self, request):
        return render(request, 'home/ripe_view.html')  
        
class RouteView(View):
    def get(self, request):
        return render(request, 'home/route_view.html') 

class Documentations(View):
    def get(self, request):
        return render(request, 'home/documentation.html')

class InstallView(View):
    def get(self, request):
        return render(request, 'home/install.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'home/contact.html')

def filter(request,filter_by):
    print(filter_by)
    dic= {
        1: "router chicago and",
        2: "router amsix and",
        3: "router linx and",
        4: "collector rrc00 and",
        5: "collector rrc01 and",
        6: "collector rrc12 and"
    }
    context = {
        "filter_name":dic[filter_by]
    }
    return render(request, 'home/filters.html',context)