from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from IncidentLog.models import IncidentLog
from IncidentLocation.views import expectedAttr as loc_expectedAttr
from IncidentLocation.models import IncidentLocation
from models import Incident

from common import util, commonHttp
import logging
import json
import datetime


# attributes of Incident
expectedAttr = {
	'ACT_TIME' : 'activation_time',
	'DEACT_TIME' : 'deactivation_time',
	'DESC' : 'description',
	'TYPE' : 'incident_type',
	'LOC' : 'location'
}


logger = logging.getLogger("django")


def create_location(loc_obj):

	loc_req_attrs = [
		loc_expectedAttr["RADIUS"],
		loc_expectedAttr["COORD_LAT"],
		loc_expectedAttr["COORD_LONG"],
	]
	
	commonHttp.check_keys(loc_obj, loc_req_attrs)

	new_location = IncidentLocation(
		radius=loc_obj[loc_expectedAttr["RADIUS"]],
		coord_lat=loc_obj[loc_expectedAttr["COORD_LAT"]],
		coord_long=loc_obj[loc_expectedAttr["COORD_LONG"]])
		
	commonHttp.save_model_obj(new_location)
	
	return new_location
	
def incident_to_obj(incident_model):
	
	location = None
	
	if incident_model.location:
		location = {
			loc_expectedAttr["RADIUS"] : incident_model.location.radius,
			loc_expectedAttr["COORD_LAT"] : incident_model.location.coord_lat,
			loc_expectedAttr["COORD_LONG"] : incident_model.location.coord_long,
		}
	
	return {
		expectedAttr["ACT_TIME"]: incident_model.activation_time, 
		expectedAttr["DEACT_TIME"]: incident_model.deactivation_time,
		expectedAttr["DESC"]: incident_model.description, 
		expectedAttr["TYPE"]: incident_model.incident_type,
		expectedAttr["LOC"]: location,
		}
		
@require_POST
@csrf_exempt
def create(request):
	"""Create Incident with IncidentLocation"""
	try:
		json_obj = commonHttp.get_json(request.body)

		# Check request json
		req_attrs = [
			expectedAttr["DESC"],
			expectedAttr["TYPE"],
			expectedAttr["LOC"],
			]

		commonHttp.check_keys(json_obj, req_attrs)

		new_location = None
		
		if json_obj.get(expectedAttr["LOC"]):
			new_location = create_location(json_obj.get(expectedAttr["LOC"]))

		activation_time = json_obj.get(expectedAttr["ACT_TIME"])
		deactivation_time = json_obj.get(expectedAttr["DEACT_TIME"])

		new_incident = Incident(
			activation_time=activation_time,
			deactivation_time=deactivation_time,
			description=json_obj[expectedAttr["DESC"]],
			incident_type=json_obj[expectedAttr["TYPE"]],
			location=new_location
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
		response_dict = util.merge_dicts(
			incident_to_obj(incident),
			{
				"success" : True,
			})
		response = JsonResponse(response_dict)

		return response

	except Incident.DoesNotExist as e:
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
			
		loc_req_attrs = [
			loc_expectedAttr["RADIUS"],
			loc_expectedAttr["COORD_LAT"],
			loc_expectedAttr["COORD_LONG"],
			]
		
		activation_time = json_obj.get(expectedAttr["ACT_TIME"])
		deactivation_time = json_obj.get(expectedAttr["DEACT_TIME"])
		description = json_obj.get(expectedAttr["DESC"])
		incident_type = json_obj.get(expectedAttr["TYPE"])
		loc_obj = json_obj.get(expectedAttr["LOC"])
			
		if activation_time:
			existing_incident.activation_time = activation_time
		if deactivation_time:
			existing_incident.deactivation_time = deactivation_time
		if description:
			existing_incident.description = description
		if incident_type:
			existing_incident.incident_type = incident_type
		if loc_obj:
			commonHttp.check_keys(loc_obj, loc_req_attrs)
			existing_incident.location.radius = loc_obj[loc_expectedAttr["RADIUS"]]
			existing_incident.location.coord_lat = loc_obj[loc_expectedAttr["COORD_LAT"]]
			existing_incident.location.coord_long = loc_obj[loc_expectedAttr["COORD_LONG"]]
			commonHttp.save_model_obj(existing_incident.location)
		
		commonHttp.save_model_obj(existing_incident)

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
		incident_json = util.merge_dicts(
			{
				"id" : incident.id,
			},
			incident_to_obj(incident))

		json_results.append(incident_json)

	response = JsonResponse({
		"results" : json_results,
		"success" : True,
		})

	return response
	