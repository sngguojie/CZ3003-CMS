from django.shortcuts import render
from django.http import HttpResponse
from models import Agency
import json
from django.views.decorators.csrf import csrf_exempt

from common import util

def is_json(json_str):
	return util.is_json(json_str)

# attributes of Agency
NAME = 'name'
DESC = 'description'
SMS_CONTACT_NO = 'sms_contact_no'
ID = 'agency_id'

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
		AGENCY_ATTR = [NAME, DESC, SMS_CONTACT_NO]
		for attr in AGENCY_ATTR:
			has_required_attr = has_required_attr and (attr in data_object)
		if not has_required_attr:
			response['error'] = 'JSON does not have required attr'
			response_json = json.dumps(response)
			return HttpResponse(response_json)	


		new_agency = Agency.create(
			name=data_object[NAME], 
			description=data_object[DESC],
			sms_contact_no=data_object[SMS_CONTACT_NO]
			)
		new_agency.save()

		response['id'] = new_agency.id
		response['success'] = True

		response_json = json.dumps(response)
		return HttpResponse(response_json)

	else:
		response['error'] = 'Not a POST request'
		response_json = json.dumps(response)
		return HttpResponse(response_json)	

csrf_exempt
def read(request):
	response = {}
	if request.method == 'POST':
		data = request.POST.get('data')
		if not is_json(data):
			response['error'] = 'Data is not in JSON'
			response_json = json.dumps(response)
			return HttpResponse(response_json)	
		data_object = json.loads(data)
		
		has_required_attr = 'agency_id' in data_object
		if not has_required_attr:
			response['error'] = 'JSON does not have required attr'
			response_json = json.dumps(response)
			return HttpResponse(response_json)	
		id_requested = data_object['agency_id']
		requested_agency= Agency.objects.get(id_requested)
		
		response['agency'] = requested_agency.__dict__
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
		AGENCY_ATTR = [NAME, DESC, SMS_CONTACT_NO]
		for attr in AGENCY_ATTR:
			has_cur_attr = (attr in data_object)
			has_required_attr = has_required_attr or has_cur_attr
			if has_cur_attr:
				attr_to_update.append(attr)
		
		has_required_attr = has_required_attr and 'agency_id' in data_object

		if not has_required_attr:
			response['error'] = 'JSON does not have required attr'
			response_json = json.dumps(response)
			return HttpResponse(response_json)	

		try:
			requested_agency = Agency.objects.get(data_object['agency_id'])
		except ValueError, e:
			response['error'] = 'Cannot find agency with requested id: '+data_object['agency_id']
			response_json = json.dumps(response)
			return HttpResponse(response_json)

		if NAME in attr_to_update:
			requested_agency.name = data_object[NAME]
			requested_agency.save()
		if DESC in attr_to_update:
			requested_agency.description = data_object[DESC]
			requested_agency.save()
		if SMS_CONTACT_NO in attr_to_update:
			requested_agency.sms_contact_no = data_object[SMS_CONTACT_NO]
			requested_agency.save()

		requested_agency.save()

		response['agency'] = requested_agency.__dict__
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
		requested_agency = Agency.objects.get(id_requested)
		

		requested_agency.delete()

		response['agency_id'] = id_requested
		response['success'] = True

		response_json = json.dumps(response)
		return HttpResponse(response_json)

	else:
		response['error'] = 'Not a POST request'
		response_json = json.dumps(response)

csrf_exempt
def list(request):
	response = {}
	if request.method == 'POST':
		
		agency_list = Agency.objects.all()

		agency_dict_list = []
		for agency in agency_list:
			agency_dict_list.append(agency.__dict__)


		response['agency'] = agency_dict_list
		response['success'] = True

		response_json = json.dumps(response)
		return HttpResponse(response_json)

	else:
		response['error'] = 'Not a POST request'
		response_json = json.dumps(response)
		return HttpResponse(response_json)