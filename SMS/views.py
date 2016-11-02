from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from models import SMS

from common import util, commonHttp
import logging
import json
import requests
import env

expectedAttr = {
	'TO': "to",
	'TITLE': "title",
	'MESSAGE': "message",
}

logger = logging.getLogger("django")

@require_POST
@csrf_exempt
def create(request):
	try:
		json_obj = commonHttp.get_json(request.body)

		req_attrs = [
			expectedAttr["TO"], 
			expectedAttr["TITLE"], 
			expectedAttr["MESSAGE"]
			]

		commonHttp.check_keys(json_obj, req_attrs)

		new_sms = SMS(
			to=json_obj[expectedAttr["TO"]],
			title=json_obj[expectedAttr["TITLE"]],
			message=json_obj[expectedAttr["MESSAGE"]]
			)

		commonHttp.save_model_obj(new_sms)

		url = "http://smsgateway.me/api/v3/messages/send"
		data = {'email':'xiaojia1993@gmail.com', 'password':env.SMS_ACC_PASSWORD,'device':'32326','number': json_obj[expectedAttr["TO"]],'message': json_obj[expectedAttr["TITLE"]] + "," +json_obj[expectedAttr["MESSAGE"]]}

		r=requests.post(url, data)
		print "test"
		print r.json()['success']

		if r.json()['success']==True:
   			status=True
		else:
   			status=False


		response = JsonResponse({
			"id" : new_sms.id,
			"success" : status
			})

		return response

	except commonHttp.HttpBadRequestException as e:
		return HttpResponseBadRequest(e.reason_phrase)


