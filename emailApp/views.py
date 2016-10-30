from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from CMSStatus.models import CMSStatus
from django.core.mail import EmailMessage
from datetime import datetime, timedelta

from common import util, commonHttp, datetime_util
import logging
import json
import requests


expectedAttr = {
	'TO': "to",
	'TITLE': "title",
	'BODY': "body",
}

@require_POST
@csrf_exempt
def create(request):
	
	json_obj = commonHttp.get_json(request.body)

	req_attrs = [
		expectedAttr["TO"], 
		expectedAttr["TITLE"], 
		expectedAttr["BODY"]
	]
	commonHttp.check_keys(json_obj, req_attrs)

 	try:
	 	cms = CMSStatus.objects.get(id=1)
	 	cms.active = json_obj.get("active")
	 	cms.last_sent = json_obj.get("last_sent")

	 	time_exceeds_interval = (datetime_util.sgt_now() - cms.last_sent) > timedelta(minutes = 30)
	 	if (time_exceeds_interval and cms.active):
	 		email=EmailMessage(json_obj[expectedAttr["TITLE"]], json_obj[expectedAttr["BODY"]], to=[json_obj[expectedAttr["TO"]]])
			email.send()
		response = JsonResponse({
		 		"active" : cms.active,
		 		"success" : True,
		 		})
		return response
 	except Exception as e:
		response = JsonResponse({
		 	"success" : False,
		 	})
 		return response
