from django.shortcuts import render
from django.template import Context, loader
from django.http import HttpResponse

from .models import Crimes

def recent(request):
    crimes = Crimes.objects.filter(date__range=["2015-1-25", "2015-1-25"])
    t = loader.get_template('recent.html')
    c = Context({'crimes': crimes})
    return HttpResponse(t.render(c))
	
def index(request):
    t = loader.get_template('base.html')
    c = Context()
    return HttpResponse(t.render(c))
