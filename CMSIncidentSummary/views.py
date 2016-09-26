from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from models import IncidentSummary
import json

# check if is valid json
def is_json(json_str):
	try:
		json_object = json.loads(myjson)
	except ValueError, e:
		return False
	return True

# attributes of IncidentSummary
DATETIME = 'datetime'
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
		INCIDENT_SUMMARY_ATTR = [DATETIME, DESC]
		for attr in INCIDENT_SUMMARY_ATTR:
			has_required_attr = has_required_attr and (attr in data_object)
		if not has_required_attr:
			response['error'] = 'JSON does not have required attr'
			response_json = json.dumps(response)
			return HttpResponse(response_json)	


		new_incident_summary = IncidentSummary.create(
			datetime=data_object[DATETIME], 
			description=data_object[DESC]
			)
		new_incident.save()

		response['id'] = new_incident_summary.id
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
		try:
			requested_incident_summary = IncidentSummary.objects.get(data_object['id'])
		except ValueError, e:
			response['error'] = 'Cannot find incident with requested id: '+data_object['id']
			response_json = json.dumps(response)
			return HttpResponse(response_json)
		
		response['incident_summary'] = requested_incident_summary.__dict__
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
		INCIDENT_SUMMARY_ATTR = [DATETIME, DESC]
		for attr in INCIDENT_SUMMARY_ATTR:
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
			requested_incident_summary = IncidentSummary.objects.get(data_object['id'])
		except ValueError, e:
			response['error'] = 'Cannot find incident with requested id: '+data_object['id']
			response_json = json.dumps(response)
			return HttpResponse(response_json)

		if DATETIME in attr_to_update:
			requested_incident_summary.datetime = data_object[DATETIME]
			requested_incident_summary.save()
		
		if DESC in attr_to_update:
			requested_incident_summary.description = data_object[DESC]
			requested_incident_summary.save()

		requested_incident.save()

		response['incident_summary'] = requested_incident.__dict__
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
		requested_incident_summary = IncidentSummary.objects.get(id_requested)
		

		requested_incident_summary.delete()

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
		
		incident_summary_list = IncidentSummary.objects.all()

		incident_summaries_dict_list = []
		for incident_summary in incident_summary_list:
			incident_summaries_dict_list.append(incident_summary.__dict__)


		response['incident_summaries'] = incident_summaries_dict_list
		response['success'] = True

		response_json = json.dumps(response)
		return HttpResponse(response_json)

	else:
		response['error'] = 'Not a POST request'
		response_json = json.dumps(response)
		return HttpResponse(response_json)