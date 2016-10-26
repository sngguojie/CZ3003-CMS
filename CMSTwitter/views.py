from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from twitter_api import TwitterApp

import env

from common import util, commonHttp
import logging
import json

expectedAttr = {
	'STATUS': 'status'
}

logger = logging.getLogger("django")

twitterapp = TwitterApp(env.TWIT_CONSUMER_KEY, env.TWIT_CONSUMER_SECRET, env.TWIT_ACCESS_TOKEN, env.TWIT_ACCESS_TOKEN_SECRET)

@require_POST
@csrf_exempt
def update(request):
	try:
		json_obj = commonHttp.get_json(request.body)
		
		req_attrs = [
			expectedAttr['STATUS'],
			]

		commonHttp.check_keys(json_obj, req_attrs)

		status = json_obj.get(expectedAttr['STATUS'])
		
		updated_status = twitterapp.update_status(status)
		
		response = JsonResponse({
			"success" : True,
			})

		return response

	except commonHttp.HttpBadRequestException as e:
		return HttpResponseBadRequest(e.reason_phrase)