from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from models import Incident

from common import util
import logging
import json


# attributes of Incident
expectedAttr = {
	'ACT_TIME' = 'activation_time',
	'DEACT_TIME' = 'deactivation_time',
	'DESC' = 'description',
	'ID' = 'id',
}


logger = logging.getLogger("django")

@require_POST
@csrf_exempt
def create(request):
	try:
		json_obj = commonHttp.get_json(request.body)

		req_attrs = [
			expectedAttr["ACT_TIME"], 
			expectedAttr["DEACT_TIME"], 
			expectedAttr["DESC"],
			]

		commonHttp.check_keys(json_obj, req_attrs)

		new_incident = Incident(
			activation_time=json_obj[expectedAttr["ACT_TIME"]],
			deactivation_time=json_obj[expectedAttr["DEACT_TIME"]],
			description=json_obj[expectedAttr["DESC"]],
			)

		commonHttp.save_model_obj(new_incident)

		response = JsonResponse({
			"id" : new_incident.id,
			"success" : True
			})

		return response

	except commonHttp.HttpBadRequestException as e:
		return HttpResponseBadRequest(e.reason_phrase)
	

@require_GET	
@csrf_exempt
def read(request, obj_id):
	try:
		incident = Incident.objects.get(id=obj_id)
		response = JsonResponse({
			expectedAttr["ACT_TIME"]: incident.activation_time, 
			expectedAttr["DEACT_TIME"]: incident.deactivation_time,
			expectedAttr["DESC"]: incident.description, 
			"success" : True,
			})

		return response

	except IncidentCallReport.DoesNotExist as e:
		return HttpResponseBadRequest(str(e))


@require_POST
@csrf_exempt
def update(request, obj_id):
	try:
		# Get existing obj
		existing_incident= Incident.objects.get(id=obj_id)
	except Incident.DoesNotExist as e:
		return HttpResponseBadRequest(str(e))
	try:
		# Update existing obj
		json_obj = commonHttp.get_json(request.body)

		req_attrs = [
			expectedAttr["ACT_TIME"], 
			expectedAttr["DEACT_TIME"], 
			expectedAttr["DESC"],
			]

		commonHttp.check_keys(json_obj, req_attrs)

		existing_incident.activation_time = json_obj.get(expectedAttr["ACT_TIME"])
		existing_incident.deactivation_time = json_obj.get(expectedAttr["DEACT_TIME"])
		existing_incident.description = json_obj.get(expectedAttr["DESC"])
		
		commonHttp.save_model_obj(existing_icr)

		response = JsonResponse({
			"success" : True,
			})

		return response

	except commonHttp.HttpBadRequestException as e:
		return HttpResponseBadRequest(e.reason_phrase)

	
require_POST
@csrf_exempt
def delete(request, obj_id):
	try:
		# Get existing obj
		existing_incident= Incident.objects.get(id=obj_id)
	except Incident.DoesNotExist as e:
		return HttpResponseBadRequest(str(e))
	existing_incident.delete()
	response = JsonResponse({
		"success" : True,
		})

	return response 
	

@require_GET
@csrf_exempt
def list(request):
	all_incidents = Incident.objects.all()

	json_results = []

	for incident in all_incidents:
		incident_json = {
			"id" : incident.id,
			expectedAttr["CALLER_NAME"]: incident.activation_time, 
			expectedAttr["CALLER_NRIC"]: incident.deactivation_time, 
			expectedAttr["DESC"]: incident.description, 
			
		}

		json_results.append(incident_json)

	response = JsonResponse({
		"results" : json_results,
		"success" : True,
		})

	return response
	