from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST

from models import IncidentLocation

from common import util, commonHTTP
import logging
import json

expectedAttr = {
	'RADIUS': "radius",
	'COORD_LAT': "coord_lat",
	'COORD_LONG': "coord_long"
}

logger = logging.getLogger("django")

@require_POST
@csrf_exempt
def create(request):
	json_obj = json.loads(request.body)

	req_attrs = [
		expectedAttr["RADIUS"], 
		expectedAttr["COORD_LAT"], 
		expectedAttr["COORD_LONG"]
		]

	has_key, missing_key = util.check_keys(json_obj, req_attrs)
	if not has_key:
		return commonHTTP.makeMissingAttrResponse(missing_key)

	new_loc = IncidentLocation(
		radius=json_obj[expectedAttr["RADIUS"]],
		coord_lat=json_obj[expectedAttr["COORD_LAT"]],
		coord_long=json_obj[expectedAttr["COORD_LONG"]]
		)

	new_loc.save()

	response = {}
	response["id"] = new_loc.id
	response["success"] = True

	return HttpResponse(json.dumps(response))


@require_GET
def read(request):
	pass

@require_POST
def update(request):
	pass

@require_POST
def delete(request):
	pass

@require_GET
def list(request):
	pass