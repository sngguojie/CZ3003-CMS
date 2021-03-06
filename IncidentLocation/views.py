from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from models import IncidentLocation

from common import util, commonHttp
import logging
import json

expectedAttr = {
	'RADIUS': "radius",
	'COORD_LAT': "coord_lat",
	'COORD_LONG': "coord_long",
}

logger = logging.getLogger("django")

@require_POST
@csrf_exempt
def create(request):
	try:
		json_obj = commonHttp.get_json(request.body)

		req_attrs = [
			expectedAttr["RADIUS"], 
			expectedAttr["COORD_LAT"], 
			expectedAttr["COORD_LONG"]
			]

		commonHttp.check_keys(json_obj, req_attrs)

		new_loc = IncidentLocation(
			radius=json_obj[expectedAttr["RADIUS"]],
			coord_lat=json_obj[expectedAttr["COORD_LAT"]],
			coord_long=json_obj[expectedAttr["COORD_LONG"]]
			)

		commonHttp.save_model_obj(new_loc)

		response = JsonResponse({
			"id" : new_loc.id,
			"success" : True
			})

		return response

	except commonHttp.HttpBadRequestException as e:
		return HttpResponseBadRequest(e.reason_phrase)


@require_GET
@csrf_exempt
def read(request, obj_id):
	try:
		loc = IncidentLocation.objects.get(id=obj_id)
		response = JsonResponse({
			expectedAttr["RADIUS"] : loc.radius,
			expectedAttr["COORD_LAT"] : loc.coord_lat,
			expectedAttr["COORD_LONG"] : loc.coord_long,
			"success" : True,
			})

		return response

	except IncidentLocation.DoesNotExist as e:
		return HttpResponseBadRequest(str(e))

@require_POST
@csrf_exempt
def update(request, obj_id):
	try:
		# Get existing obj
		existing_loc = IncidentLocation.objects.get(id=obj_id)
	except IncidentLocation.DoesNotExist as e:
		return HttpResponseBadRequest(str(e))

	try:
		# Update existing obj
		json_obj = commonHttp.get_json(request.body)

		req_attrs = [
			expectedAttr["RADIUS"],
			expectedAttr["COORD_LAT"],
			expectedAttr["COORD_LONG"],
			]

		commonHttp.check_keys(json_obj, req_attrs)

		existing_loc.radius = json_obj.get(expectedAttr["RADIUS"])
		existing_loc.coord_lat = json_obj.get(expectedAttr["COORD_LAT"])
		existing_loc.coord_long = json_obj.get(expectedAttr["COORD_LONG"])

		commonHttp.save_model_obj(existing_loc)

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
		existing_loc = IncidentLocation.objects.get(id=obj_id)
	except IncidentLocation.DoesNotExist as e:
		return HttpResponseBadRequest(str(e))

	existing_loc.delete()
	response = JsonResponse({
		"success" : True,
		})

	return response 

@require_GET
@csrf_exempt
def list(request):
	all_loc = IncidentLocation.objects.all()

	json_results = []

	for loc in all_loc:
		loc_json = {
			"id" : loc.id,
			expectedAttr["RADIUS"] : loc.radius,
			expectedAttr["COORD_LAT"] : loc.coord_lat,
			expectedAttr["COORD_LONG"] : loc.coord_long,
		}

		json_results.append(loc_json)

	response = JsonResponse({
		"results" : json_results,
		"success" : True,
		})

	return response