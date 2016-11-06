from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from CMSStatus.models import CMSStatus
from django.core.mail import EmailMessage
from datetime import datetime, timedelta
from IncidentLog.models import IncidentLog
from Incident.models import Incident
from IncidentSummary.models import IncidentSummary

from common import util, commonHttp, datetime_util
import logging
import json
import requests


expectedAttr = {
	'TO': "to",
	'TITLE': "title",
	'BODY': "body",
}

cmsexpectedAttr = {
	'ACTIVE': "active"
}

@require_POST
@csrf_exempt
def create(request):	
	json_obj = commonHttp.get_json(request.body)


 	try:
	 	cms = CMSStatus.objects.get(id=1)
	 	all_incident_logs = IncidentLog.objects.all()
	 	contentStr=''
	 	currentPointer=-1
	 	for incident_logs in reversed(all_incident_logs):

	 		incident = Incident.objects.get(id=incident_logs.incident_id)
	 		if currentPointer!=incident_logs.incident_id:
	 			contentStr= contentStr + '\nIncident ID and Type: ' + str(incident_logs.incident_id) + ' ' + incident.incident_type + '\nDescription: ' + incident_logs.description + '\nDateTime: ' + str(incident_logs.datetime) +'\n'
	 			currentPointer=incident_logs.incident_id
	 		else:
	 			contentStr= contentStr + 'Description: ' + incident_logs.description + '\nDateTime: ' + str(incident_logs.datetime) +'\n'

		time_difference=datetime_util.sgt_now() - cms.last_sent
		
	 	if time_difference > timedelta(minutes=30) and cms.active:
	 		email=EmailMessage('Incident Report Generated ' + str(datetime_util.sgt_now()), contentStr, to=['jqlee93@gmail.com'])
			email.send()
			cms.last_sent=datetime_util.sgt_now()
			commonHttp.save_model_obj(cms)
			new_ism = IncidentSummary(
				description=contentStr,
				datetime=datetime_util.sgt_now()
				)
			commonHttp.save_model_obj(new_ism)

		response = JsonResponse({
		 	cmsexpectedAttr["ACTIVE"] : cms.active,
		 	"cms_last_sent": cms.last_sent,
		 	"success" : True,
		 	})
		return response
 	except Exception as e:
		response = JsonResponse({
			cmsexpectedAttr["ACTIVE"] : cms.active,
			"cms_last_sent": cms.last_sent,
		 	"success" : False,
		 	"exception": e,
		 	})
 		return response
