
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from models import IncidentSummary

from common import util, commonHttp
import logging
import json



# attributes of IncidentSummary
expectedAttr = {
	'DATETIME': "datetime",
	'DESC': "description",
	'ID': "id",
}

logger = logging.getLogger("django")

# Create your views here.
@require_POST
@csrf_exempt
def create(request):
	try:
		json_obj = commonHttp.get_json(request.body)

		req_attrs = [
			expectedAttr["DESC"], 
			expectedAttr["DATETIME"]
			]

		commonHttp.check_keys(json_obj, req_attrs)

		new_ism = IncidentSummary(
			description=json_obj[expectedAttr["DESC"]],
			datetime=json_obj[expectedAttr["DATETIME"]]
			)

		commonHttp.save_model_obj(new_ism)

		response = JsonResponse({
			"id" : new_ism.id,
			"success" : True
			})

		return response

	except commonHttp.HttpBadRequestException as e:
		return HttpResponseBadRequest(e.reason_phrase)

	
@require_GET
@csrf_exempt
def read(request, obj_id):
	try:
		icr = IncidentSummary.objects.get(id=obj_id)
		response = JsonResponse({
			expectedAttr["DESC"]: icr.description, 
			expectedAttr["DATETIME"]: icr.dateTime,
			"success" : True,
			})

		return response

	except IncidentSummary.DoesNotExist as e:
		return HttpResponseBadRequest(str(e))
	

@require_POST
@csrf_exempt
def update(request, obj_id):
	try:
		# Get existing obj
		existing_ism= IncidentSummary.objects.get(id=obj_id)
	except IncidentSummary.DoesNotExist as e:
		return HttpResponseBadRequest(str(e))

	try:
		# Update existing obj
		json_obj = commonHttp.get_json(request.body)

		req_attrs = [
			expectedAttr["DESC"], 
			expectedAttr["DATETIME"]
			]

		commonHttp.check_keys(json_obj, req_attrs)

		existing_ism.description = json_obj.get(expectedAttr["DESC"])
		existing_ism.dateTime = json_obj.get(expectedAttr["DATETIME"])

		commonHttp.save_model_obj(existing_ism)

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
		existing_ism= IncidentSummary.objects.get(id=obj_id)
	except IncidentSummary.DoesNotExist as e:
		return HttpResponseBadRequest(str(e))

	existing_ism.delete()
	response = JsonResponse({
		"success" : True,
		})

	return response 


@require_GET
@csrf_exempt
def list(request):
	all_ism = IncidentSummary.objects.all()

	json_results = []

	for ism in all_ism:
		ism_json = {
			"id" : ism.id,
			expectedAttr["DESC"]: ism.description, 
			expectedAttr["DATETIME"]: ism.dateTime,
		}

		json_results.append(ism_json)

	response = JsonResponse({
		"results" : json_results,
		"success" : True,
		})

	return response	
	