from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse


from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login

from common import util, commonHttp
import logging
import json

logger = logging.getLogger("django")

expectedAttr = {
	'USERNAME' : 'username',
	'PASSWORD' : 'password',
	'ID' : 'id',
}


@require_POST
@csrf_exempt
def login_view(request):
	try:
		json_obj = commonHttp.get_json(request.body)

		req_attrs = [
			expectedAttr['USERNAME'], 
			expectedAttr['PASSWORD'], 
			]

		commonHttp.check_keys(json_obj, req_attrs)

		user = authenticate(username=json_obj[expectedAttr['USERNAME']], password=json_obj[expectedAttr['PASSWORD']])
		if user is None:
			# No backend authenticated the credentials
			return HttpResponseBadRequest('Login credentials invalid')
		
		# A backend authenticated the credentials
		login(request, user)
		
		groups = user.groups.all()
		groups_str = ''
		for group in groups:
			groups_str += group.name + ', '
		if not (groups_str == ''):
			groups_str = groups_str[:-2]

		response = JsonResponse({
			"id" : user.id,
			"groups": groups_str,
			"success" : True
			})

		return response

	except commonHttp.HttpBadRequestException as e:
		return HttpResponseBadRequest(e.reason_phrase)
	
