from django.shortcuts import render
from django.http import HttpResponse
import json

# Create your views here.
def create(request):
	if request.method == 'POST':
		activation_time = request.POST.get('activation_time')
		deactivation_time = request.POST.get('deactivation_time')
		description = request.POST.get('description')
		
	pass

def read(request):
	pass

def update(request):
	pass

def delete(request):
	pass

def list(request):
	pass