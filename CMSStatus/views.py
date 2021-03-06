from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from models import CMSStatus

from common import util, commonHttp, datetime_util
import logging
import json
import requests


expectedAttr = {
	'ACTIVE': "active"
}

logger = logging.getLogger("django")

@require_GET
@csrf_exempt
def read(request, obj_id):
	try:
		cms = CMSStatus.objects.get(id=obj_id)
		response = JsonResponse({
			expectedAttr["ACTIVE"] : cms.active,
			"success" : True,
			})

		return response

	except CMSStatus.DoesNotExist as e:
		return HttpResponseBadRequest(str(e))


@require_POST
@csrf_exempt
def update(request, obj_id):
	try:
		# Get existing obj
		cms = CMSStatus.objects.get(id=obj_id)
	except CMSStatus.DoesNotExist as e:
		return HttpResponseBadRequest(str(e))

	try:
		# Update existing obj
		json_obj = commonHttp.get_json(request.body)

		req_attrs = [
			expectedAttr["ACTIVE"],
			]

		commonHttp.check_keys(json_obj, req_attrs)

		cms.active = json_obj.get(expectedAttr["ACTIVE"])
		commonHttp.save_model_obj(cms)


		if cms.active==True:
			url = "https://crisismanagement.herokuapp.com/emailApp/create_for_first_time_active/"
			r=requests.post(url,json={"start": "start"})
			
		
		response = JsonResponse({
			"success" : True,
			})

		return response

	except commonHttp.HttpBadRequestException as e:
		return HttpResponseBadRequest(e.reason_phrase)