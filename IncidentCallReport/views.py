from django.shortcuts import render

# Create your views here.

def create(request):
	if request.method == 'POST':
		caller_name = request.POST.get('caller_name')
		caller_nric = request.POST.get('caller_nric')
		contact_no = request.POST.get('contact_no')
		description = request.POST.get('description')
		incident_type = request.POST.get('incident_type')
		dateTime = request.POST.get('dateTime')
		
	pass

def read(request):
	pass

def update(request):
	pass

def delete(request):
	pass

def list(request):
	pass
