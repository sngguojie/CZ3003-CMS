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
}


@require_POST
@csrf_exempt
def create(request):
	try:
		json_obj = commonHttp.get_json(request.body)

		req_attrs = [
			expectedAttr["INCIDENT_ID"], 
			expectedAttr["DESCRIPTION"]
			]

		commonHttp.check_keys(json_obj, req_attrs)

		new_log = IncidentLog(
			incident_id=json_obj[expectedAttr["INCIDENT_ID"]],
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
