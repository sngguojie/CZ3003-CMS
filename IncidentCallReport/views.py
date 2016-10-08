
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from models import IncidentCallReport

from common import util, commonHttp
import logging
import json

expectedAttr = {
	'CALLER_NAME': "caller_name",
	'CALLER_NRIC': "caller_nric",
	'CONTACT_NO': "contact_no",
	'DESC': "description",
	'TYPE': "incident_type",
	'DATETIME': "dateTime",
}

logger = logging.getLogger("django")

@require_POST
@csrf_exempt
def create(request):
	try:
		json_obj = commonHttp.get_json(request.body)

		req_attrs = [
			expectedAttr["CALLER_NAME"], 
			expectedAttr["CALLER_NRIC"], 
			expectedAttr["CONTACT_NO"],
			expectedAttr["DESC"], 
			expectedAttr["TYPE"], 
			expectedAttr["DATETIME"]
			]

		commonHttp.check_keys(json_obj, req_attrs)

		new_icr = IncidentCallReport(
			caller_name=json_obj[expectedAttr["CALLER_NAME"]],
			caller_nric=json_obj[expectedAttr["CALLER_NRIC"]],
			contact_no=json_obj[expectedAttr["CONTACT_NO"]],
			description=json_obj[expectedAttr["DESC"]],
			incident_type=json_obj[expectedAttr["TYPE"]],
			dateTime=json_obj[expectedAttr["DATETIME"]]
			)

		commonHttp.save_model_obj(new_icr)

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
			expectedAttr["CALLER_NRIC"]: icr.caller_nric, 
			expectedAttr["CONTACT_NO"]: icr.contact_no,
			expectedAttr["DESC"]: icr.description, 
			expectedAttr["TYPE"]: icr.incident_type, 
			expectedAttr["DATETIME"]: icr.dateTime,
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
			expectedAttr["CALLER_NRIC"], 
			expectedAttr["CONTACT_NO"],
			expectedAttr["DESC"], 
			expectedAttr["TYPE"], 
			expectedAttr["DATETIME"]
			]

		commonHttp.check_keys(json_obj, req_attrs)

		existing_icr.caller_name = json_obj.get(expectedAttr["CALLER_NAME"])
		existing_icr.caller_nric = json_obj.get(expectedAttr["CALLER_NRIC"])
		existing_icr.contact_no = json_obj.get(expectedAttr["CONTACT_NO"])
		existing_icr.description = json_obj.get(expectedAttr["DESC"])
		existing_icr.incident_type = json_obj.get(expectedAttr["TYPE"])
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
def list(request):
	all_icr = IncidentCallReport.objects.all()

	json_results = []

	for icr in all_icr:
		icr_json = {
			"id" : icr.id,
			expectedAttr["CALLER_NAME"]: icr.caller_name, 
			expectedAttr["CALLER_NRIC"]: icr.caller_nric, 
			expectedAttr["CONTACT_NO"]: icr.contact_no,
			expectedAttr["DESC"]: icr.description, 
			expectedAttr["TYPE"]: icr.incident_type, 
			expectedAttr["DATETIME"]: icr.dateTime,
		}

		json_results.append(icr_json)

	response = JsonResponse({
		"results" : json_results,
		"success" : True,
		})

	return response