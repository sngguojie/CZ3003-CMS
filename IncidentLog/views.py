from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

import datetime
from models import IncidentLog
from common import commonHttp


expectedAttr = {
	'INCIDENT_ID': "incident_id",
	'DESCRIPTION': "description",
	'DATETIME' : "datetime",
}


@require_GET
@csrf_exempt
def get_logs_for_incident(request, incident_id):
    """Gets logs for given incident"""

    incident_logs = IncidentLog.objects.all().filter(incident_id=incident_id)

    json_results = []

    for log in incident_logs:
		log_json = {
			"id" : log.id,
			expectedAttr['INCIDENT_ID'] : log.incident_id,
			expectedAttr['DESCRIPTION'] : log.description,
			expectedAttr['DATETIME'] : log.datetime,
		}

		json_results.append(log_json)

    response = JsonResponse({
		"results" : json_results,
		"success" : True,
		})

    return response


@require_POST
@csrf_exempt
def create(request, incident_id):
	"""Create log for given incident"""
	
	try:
		json_obj = commonHttp.get_json(request.body)

		req_attrs = [
			expectedAttr["DESCRIPTION"]
			]

		commonHttp.check_keys(json_obj, req_attrs)

		new_log = IncidentLog(
			incident_id=incident_id,
			datetime=datetime.datetime.now(),
			description=json_obj[expectedAttr["DESCRIPTION"]]
			)

		commonHttp.save_model_obj(new_log)

		response = JsonResponse({
			"id" : new_log.id,
			"success" : True
			})

		return response

	except commonHttp.HttpBadRequestException as e:
		return HttpResponseBadRequest(e.reason_phrase)

@require_GET
@csrf_exempt
def list(request):
	all_incident_logs = IncidentLog.objects.all()

	json_results = []

	for incident_logs in all_incident_logs:
		agency_json = {
			"id" : incident_logs.id,
			expectedAttr["INCIDENT_ID"] : incident_logs.incident_id,
			expectedAttr["DESCRIPTION"] : incident_logs.description,
			expectedAttr["DATETIME"] : incident_logs.datetime,
		}

		json_results.append(agency_json)

	response = JsonResponse({
		"results" : json_results,
		"success" : True,
		})

	return response

