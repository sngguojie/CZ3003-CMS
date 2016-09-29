from django.shortcuts import render
from django.http import HttpResponse
from models import IncidentCallReport
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# Attributes of IncidentCallReport

ID='report_id'
CALLER_NAME='caller_name'
CALLER_NRIC='caller_nric'
CONTACT_NO='contact_no'
DESC='description'
TYPE='incident_type'
DATETIME='dateTime'

@csrf_exempt
def create(request):
	response ={}

	if request.method == 'POST':
		data = request.POST.get('data')
		if not is_json(data):
			response['error'] = 'Data is not in JSON'
			response_json = json.dumps(response)
			return HttpResponse(response_json)	
		data_object = json.loads(data)

		has_required_attr = True
		INCIDENT_CALL_ATTR = [CALLER_NAME, CALLER_NRIC, CONTACT_NO,DESC,TYPE,DATETIME]
		for attr in INCIDENT_ATTR:
			has_required_attr = has_required_attr and (attr in data_object)
		if not has_required_attr:
			response['error'] = 'JSON does not have required attr'
			response_json = json.dumps(response)
			return HttpResponse(response_json)	

		new_incident_call_report = IncidentCallReport.create(
			caller_name=data_object[CALLER_NAME]
			caller_nric=data_object[CALLER_NRIC]
			contact_no=data_object[CONTACT_NO]
			description=data_object[DESC]
			incident_type=data_object[TYPE]
			dateTime=data_object[DATETIME]
			)
		new_incident_call_report.save()


		response['report_id'] = new_incident_call_report.id
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
		
		has_required_attr = 'report_id' in data_object
		if not has_required_attr:
			response['error'] = 'JSON does not have required attr'
			response_json = json.dumps(response)
			return HttpResponse(response_json)	
		id_requested = data_object['report_id']
		requested_incident_call_report = Incident.objects.get(id_requested)
		
		response['incident_call_report'] = requested_incident_call_report.__dict__
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
		INCIDENT_CALL_REPORT_ATTR = [CALLER_NAME, CALLER_NRIC, CONTACT_NO,DESC,TYPE,DATETIME]
		for attr in INCIDENT_ATTR:
			has_cur_attr = (attr in data_object)
			has_required_attr = has_required_attr or has_cur_attr
			if has_cur_attr:
				attr_to_update.append(attr)
		
		has_required_attr = has_required_attr and 'report_id' in data_object

		if not has_required_attr:
			response['error'] = 'JSON does not have required attr'
			response_json = json.dumps(response)
			return HttpResponse(response_json)	

		try:
			requested_incident_call_report = IncidentCallReport.objects.get(data_object['report_id'])
		except ValueError, e:
			response['error'] = 'Cannot find incident call report with requested id: ' + data_object['report_id']
			response_json = json.dumps(response)
			return HttpResponse(response_json)


		# After a Report is sent, NAME and NRIC should not be able to update.

		if CONTACT_NO in attr_to_update:
			requested_incident_call_report.contact_no = data_object[CONTACT_NO]
			requested_incident_call_report.save()
		if DATETIME in attr_to_update:
			requested_incident_call_report.dateTime= data_object[DATETIME]
			requested_incident_call_report.save()
		if DESC in attr_to_update:
			requested_incident_call_report.description = data_object[DESC]
			requested_incident_call_report.save()

		requested_incident_call_report.save()

		response['incident_call_report'] = requested_incident_call_report.__dict__
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
		
		has_required_attr = 'report_id' in data_object
		if not has_required_attr:
			response['error'] = 'JSON does not have required attr'
			response_json = json.dumps(response)
			return HttpResponse(response_json)	
		id_requested = data_object['report_id']
		requested_incident_call_report = IncidentCallReport.objects.get(id_requested)
		

		requested_incident_call_report.delete()

		response['report_id'] = id_requested
		response['success'] = True

		response_json = json.dumps(response)
		return HttpResponse(response_json)

	else:
		response['error'] = 'Not a POST request'
		response_json = json.dumps(response)
		return HttpResponse(response_json)

@csrf_exempt
def list(request):
	response = {}
	if request.method == 'POST':
		
		incident_call_report_list = IncidentCallReport.objects.all()

		incident_call_report_dict_list = []
		for incidentcallreport in incident_call_report:
			incident_call_report_dict_list.append(incidentcallreport.__dict__)


		response['incident_call_report'] = incident_call_report_dict_list
		response['success'] = True

		response_json = json.dumps(response)
		return HttpResponse(response_json)

	else:
		response['error'] = 'Not a POST request'
		response_json = json.dumps(response)
		return HttpResponse(response_json)
