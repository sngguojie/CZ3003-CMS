
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from models import IncidentCallReport
from Incident.models import Incident

from common import util, commonHttp
import logging
import json

expectedAttr = {
	'CALLER_NAME': "caller_name",
	'CONTACT_NO': "contact_no",
	'DESC': "description",
	'DATETIME': "dateTime",
}

logger = logging.getLogger("django")

def make_callreport(request, incident_id):
	json_obj = commonHttp.get_json(request.body)

	req_attrs = [
		expectedAttr["CALLER_NAME"], 
		expectedAttr["CONTACT_NO"],
		expectedAttr["DESC"], 
		expectedAttr["DATETIME"],
		]

	commonHttp.check_keys(json_obj, req_attrs)

	new_icr = IncidentCallReport(
		caller_name=json_obj[expectedAttr["CALLER_NAME"]],
		contact_no=json_obj[expectedAttr["CONTACT_NO"]],
		description=json_obj[expectedAttr["DESC"]],
		dateTime=json_obj[expectedAttr["DATETIME"]],
		incident_id=incident_id
		)

	commonHttp.save_model_obj(new_icr)
	
	return new_icr


@require_POST
@csrf_exempt
def create(request, incident_id):
	try:
		incident = Incident.objects.get(id=incident_id)
	except Incident.DoesNotExist as e:
		return HttpResponseBadRequest(str(e))
	try:
		
		new_icr = make_callreport(request, incident_id)
		
		response = JsonResponse({
		"id" : new_icr.id,
		"success" : True
		})

		return response

	except commonHttp.HttpBadRequestException as e:
		return HttpResponseBadRequest(e.reason_phrase)


@require_GET
@csrf_exempt
def read(request, obj_id):
	try:
		icr = IncidentCallReport.objects.get(id=obj_id)
		response = JsonResponse({
			expectedAttr["CALLER_NAME"]: icr.caller_name, 
			expectedAttr["CONTACT_NO"]: icr.contact_no,
			expectedAttr["DESC"]: icr.description, 
			expectedAttr["DATETIME"]: icr.dateTime,
			"incident_id": icr.incident_id,
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
		existing_icr= IncidentCallReport.objects.get(id=obj_id)
	except IncidentCallReport.DoesNotExist as e:
		return HttpResponseBadRequest(str(e))

	try:
		# Update existing obj
		json_obj = commonHttp.get_json(request.body)

		req_attrs = [
			expectedAttr["CALLER_NAME"], 
			expectedAttr["CONTACT_NO"],
			expectedAttr["DESC"], 
			expectedAttr["DATETIME"]
			]

		commonHttp.check_keys(json_obj, req_attrs)

		existing_icr.caller_name = json_obj.get(expectedAttr["CALLER_NAME"])
		existing_icr.contact_no = json_obj.get(expectedAttr["CONTACT_NO"])
		existing_icr.description = json_obj.get(expectedAttr["DESC"])
		existing_icr.dateTime = json_obj.get(expectedAttr["DATETIME"])

		commonHttp.save_model_obj(existing_icr)

		response = JsonResponse({
			"success" : True,
			})

		return response

	except commonHttp.HttpBadRequestException as e:
		return HttpResponseBadRequest(e.reason_phrase)

@require_POST
@csrf_exempt
def delete(request, obj_id):
	try:
		# Get existing obj
		existing_icr= IncidentCallReport.objects.get(id=obj_id)
	except IncidentCallReport.DoesNotExist as e:
		return HttpResponseBadRequest(str(e))

	existing_icr.delete()
	response = JsonResponse({
		"success" : True,
		})

	return response

@require_GET
@csrf_exempt
def list(request, incident_id):
	try:
		incident = Incident.objects.get(id=incident_id)
	except Incident.DoesNotExist as e:
		return HttpResponseBadRequest(str(e))
	try:
		all_icr = IncidentCallReport.objects.filter(incident_id=incident_id)
	
		json_results = []
	
		for icr in all_icr:
			icr_json = {
				"id" : icr.id,
				expectedAttr["CALLER_NAME"]: icr.caller_name, 
				expectedAttr["CONTACT_NO"]: icr.contact_no,
				expectedAttr["DESC"]: icr.description, 
				expectedAttr["DATETIME"]: icr.dateTime,
				"incident_id": icr.incident_id,
			}
	
			json_results.append(icr_json)
	
		response = JsonResponse({
			"results" : json_results,
			"success" : True,
			})
	
		return response
	except commonHttp.HttpBadRequestException as e:
		return HttpResponseBadRequest(e.reason_phrase)
		
