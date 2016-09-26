from django.shortcuts import render
from django.http import HttpResponse
from models import Incident
import json

# check if is valid json
def is_json(json_str):
	try:
		json_object = json.loads(myjson)
	except ValueError, e:
		return False
	return True

# attributes of Incident
ACT_TIME = 'activation_time'
DEACT_TIME = 'deactivation_time'
DESC = 'description'
ID = 'id'



# Create your views here.
@csrf_exempt
def create(request):
	response = {}
	if request.method == 'POST':
		data = request.POST.get('data')
		if not is_json(data):
			response['error'] = 'Data is not in JSON'
			response_json = json.dumps(response)
			return HttpResponse(response_json)	
		data_object = json.loads(data)
		
		has_required_attr = True
		INCIDENT_ATTR = [ACT_TIME, DEACT_TIME, DESC]
		for attr in INCIDENT_ATTR:
			has_required_attr = has_required_attr and (attr in data_object)
		if not has_required_attr:
			response['error'] = 'JSON does not have required attr'
			response_json = json.dumps(response)
			return HttpResponse(response_json)	


		new_incident = Incident.create(
			activation_time=data_object[ACT_TIME], 
			deactivation_time=data_object[DEACT_TIME], 
			description=data_object[DESC]
			)
		new_incident.save()

		response['id'] = new_incident.id
		response['success'] = True

		response_json = json.dumps(response)
		return HttpResponse(response_json)

	else:
		response['error'] = 'Not a POST request'
		response_json = json.dumps(response)
		return HttpResponse(response_json)	
	
@csrf_exempt
def read(request):
	response = {}
	if request.method == 'POST':
		data = request.POST.get('data')
		if not is_json(data):
			response['error'] = 'Data is not in JSON'
			response_json = json.dumps(response)
			return HttpResponse(response_json)	
		data_object = json.loads(data)
		
		has_required_attr = 'id' in data_object
		if not has_required_attr:
			response['error'] = 'JSON does not have required attr'
			response_json = json.dumps(response)
			return HttpResponse(response_json)	
		id_requested = data_object['id']
		requested_incident = Incident.objects.get(id_requested)
		
		response['incident'] = requested_incident.__dict__
		response['success'] = True

		response_json = json.dumps(response)
		return HttpResponse(response_json)

	else:
		response['error'] = 'Not a POST request'
		response_json = json.dumps(response)
		return HttpResponse(response_json)	
	
@csrf_exempt
def update(request):
	response = {}
	if request.method == 'POST':
		data = request.POST.get('data')
		if not is_json(data):
			response['error'] = 'Data is not in JSON'
			response_json = json.dumps(response)
			return HttpResponse(response_json)	
		data_object = json.loads(data)
		
		attr_to_update = []
		has_required_attr = False
		INCIDENT_ATTR = [ACT_TIME, DEACT_TIME, DESC]
		for attr in INCIDENT_ATTR:
			has_cur_attr = (attr in data_object)
			has_required_attr = has_required_attr or has_cur_attr
			if has_cur_attr:
				attr_to_update.append(attr)
		
		has_required_attr = has_required_attr and 'id' in data_object

		if not has_required_attr:
			response['error'] = 'JSON does not have required attr'
			response_json = json.dumps(response)
			return HttpResponse(response_json)	

		try:
			requested_incident = Incident.objects.get(data_object['id'])
		except ValueError, e:
			response['error'] = 'Cannot find incident with requested id: '+data_object['id']
			response_json = json.dumps(response)
			return HttpResponse(response_json)

		if ACT_TIME in attr_to_update:
			requested_incident.activation_time = data_object[ACT_TIME]
			requested_incident.save()
		if DEACT_TIME in attr_to_update:
			requested_incident.deactivation_time = data_object[DEACT_TIME]
			requested_incident.save()
		if DESC in attr_to_update:
			requested_incident.description = data_object[DESC]
			requested_incident.save()

		requested_incident.save()

		response['incident'] = requested_incident.__dict__
		response['success'] = True

		response_json = json.dumps(response)
		return HttpResponse(response_json)

	else:
		response['error'] = 'Not a POST request'
		response_json = json.dumps(response)
		return HttpResponse(response_json)

@csrf_exempt
def delete(request):
	response = {}
	if request.method == 'POST':
		data = request.POST.get('data')
		if not is_json(data):
			response['error'] = 'Data is not in JSON'
			response_json = json.dumps(response)
			return HttpResponse(response_json)	
		data_object = json.loads(data)
		
		has_required_attr = 'id' in data_object
		if not has_required_attr:
			response['error'] = 'JSON does not have required attr'
			response_json = json.dumps(response)
			return HttpResponse(response_json)	
		id_requested = data_object['id']
		requested_incident = Incident.objects.get(id_requested)
		

		requested_incident.delete()

		response['id'] = id_requested
		response['success'] = True

		response_json = json.dumps(response)
		return HttpResponse(response_json)

	else:
		response['error'] = 'Not a POST request'
		response_json = json.dumps(response)
		return HttpResponse(response_json)

def list(request):
	response = {}
	if request.method == 'POST':
		
		incidents_list = Incident.objects.all()

		incidents_dict_list = []
		for incident in incidents_list:
			incidents_dict_list.append(incident.__dict__)


		response['incidents'] = incidents_dict_list
		response['success'] = True

		response_json = json.dumps(response)
		return HttpResponse(response_json)

	else:
		response['error'] = 'Not a POST request'
		response_json = json.dumps(response)
		return HttpResponse(response_json)