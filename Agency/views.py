from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from models import Agency

from common import util, commonHttp
import logging
import json

expectedAttr = {
	'NAME': "name",
	'DESCRIPTION': "description",
	'SMS_CONTACT_NO': "sms_contact_no",
}


logger = logging.getLogger("django")

@require_POST
@csrf_exempt
def create(request):
	try:
		json_obj = commonHttp.get_json(request.body)

		req_attrs = [
			expectedAttr["NAME"], 
			expectedAttr["DESCRIPTION"], 
			expectedAttr["SMS_CONTACT_NO"]
			]

		commonHttp.check_keys(json_obj, req_attrs)

		new_agency = Agency(
			name=json_obj[expectedAttr["NAME"]],
			description=json_obj[expectedAttr["DESCRIPTION"]],
			sms_contact_no=json_obj[expectedAttr["SMS_CONTACT_NO"]]
			)

		commonHttp.save_model_obj(new_agency)

		response = JsonResponse({
			"id" : new_agency.id,
			"success" : True
			})

		return response

	except commonHttp.HttpBadRequestException as e:
		return HttpResponseBadRequest(e.reason_phrase)


@require_GET
@csrf_exempt
def read(request, obj_id):
	try:
		agency = Agency.objects.get(id=obj_id)
		response = JsonResponse({
			expectedAttr["NAME"] : agency.name,
			expectedAttr["DESCRIPTION"] : agency.description,
			expectedAttr["SMS_CONTACT_NO"] : agency.sms_contact_no,
			"success" : True,
			})

		return response

	except Agency.DoesNotExist as e:
		return HttpResponseBadRequest(str(e))

@require_POST
@csrf_exempt
def update(request, obj_id):
	try:
		# Get existing obj
		existing_agency = Agency.objects.get(id=obj_id)
	except Agency.DoesNotExist as e:
		return HttpResponseBadRequest(str(e))

	try:
		# Update existing obj
		json_obj = commonHttp.get_json(request.body)

		req_attrs = [
			expectedAttr["NAME"],
			expectedAttr["DESCRIPTION"],
			expectedAttr["SMS_CONTACT_NO"],
			]

		commonHttp.check_keys(json_obj, req_attrs)

		existing_agency.name = json_obj.get(expectedAttr["NAME"])
		existing_agency.desc = json_obj.get(expectedAttr["DESCRIPTION"])
		existing_agency.sms_contact_no = json_obj.get(expectedAttr["SMS_CONTACT_NO"])

		commonHttp.save_model_obj(existing_agency)

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
		existing_agency = Agency.objects.get(id=obj_id)
	except Agency.DoesNotExist as e:
		return HttpResponseBadRequest(str(e))

	existing_agency.delete()
	response = JsonResponse({
		"success" : True,
		})

	return response 

@require_GET
@csrf_exempt
def list(request):
	all_agency = Agency.objects.all()

	json_results = []

	for agency in all_agency:
		agency_json = {
			"id" : agency.id,
			expectedAttr["NAME"] : agency.name,
			expectedAttr["DESCRIPTION"] : agency.description,
			expectedAttr["SMS_CONTACT_NO"] : agency.sms_contact_no,
		}

		json_results.append(agency_json)

	response = JsonResponse({
		"results" : json_results,
		"success" : True,
		})

	return response
